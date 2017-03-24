import utime as time
import sys
import ubinascii
import ujson
import gc
import ure
import uasyncio as asyncio
import configs as confs
from rules.rule import Rule
from rules.action import Action
from rules.rule_loader import RuleLoader
from umqtt.simple import MQTTClient

client = MQTTClient(confs.CLIENT_ID, confs.HOST)
loop = asyncio.get_event_loop()
devices = {}
event_id = 0
enable = False
last_hb = time.time()

@asyncio.coroutine
def main():
    client.DEBUG = True

    client.set_callback(message_arrive)

    try:
        client.connect(clean_session=False)
    except Exception:
        print("Error while connecting to mqtt broker")
        sys.exit()
    print("Connected to {}".format(confs.HOST))

    # Load json rules
    RuleLoader.process_rules()
    print('Hellooo')
    client.subscribe(confs.SUB_TOPIC)

    loop.create_task(wait_message())
    loop.create_task(heart_beat())

    yield from asyncio.sleep(0)


@asyncio.coroutine
def wait_message():
    while True:
        client.wait_msg()
        yield from asyncio.sleep(0.001)


@asyncio.coroutine
def heart_beat():
    while True:
        global enable

        if ((int(time.time()) - int(last_hb)) > 6):
            print('GatewayCEP - UP')
            enable = True
        else:
            print('GatewayCEP - DOWN')
            enable = False
        yield from asyncio.sleep(5)


def message_arrive(topic, msg):
    if topic.decode("utf-8") == confs.HB_TOPIC:
        global last_hb
        last_hb = time.time()
        return

    if not enable:
        #print('ignored')
        return

    if(gc.mem_alloc()>2000000):
        gc.collect()
        print(gc.mem_alloc())

    message = ujson.loads(msg)
    for reg_topic in Rule.actions_list.keys():
        regex = ure.compile(reg_topic)
        if regex.match(topic.decode("utf-8")):
            if not isinstance(Rule.actions_list[reg_topic], list):
                loop.create_task(Rule.actions_list[reg_topic].process_event(message, client))

            else:
                for action in Rule.actions_list[reg_topic]:
                    loop.create_task(action.process_event(message, client))

if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()
    loop.close()
