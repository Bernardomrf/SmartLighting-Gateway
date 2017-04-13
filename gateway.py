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
client_pub = MQTTClient(confs.CLIENT_ID_PUB, confs.HOST_PUB)
client_pub.connect()
loop = asyncio.get_event_loop()
enable = False
last_hb = time.time()

@asyncio.coroutine
def main():

    client.set_callback(message_arrive)
    client.connect()
    client.subscribe(confs.SUB_TOPIC)
    client.subscribe(confs.HB_TOPIC)

    RuleLoader.process_rules()

    loop.create_task(wait_message())
    loop.create_task(heart_beat())

    yield from asyncio.sleep(0)


@asyncio.coroutine
def wait_message():
    while True:
        yield client.wait_msg()
        #yield from asyncio.sleep(0.1) #Needed to check heart beat (0 or 0.001)


@asyncio.coroutine
def heart_beat():
    while True:
        global enable

        if ((time.time() - last_hb) > confs.HB_TIMER):
            print('GatewayCEP - UP')
            enable = True
        else:
            print('GatewayCEP - DOWN')
            enable = False
        yield from asyncio.sleep(confs.HB_TIMER)


def message_arrive(topic, msg):

    if topic.decode("utf-8") == confs.HB_TOPIC:
        global last_hb
        last_hb = time.time()
        return

    if not enable:
        return

    if(gc.mem_alloc()>confs.MAX_MEM):
        gc.collect()
        print(gc.mem_alloc())

    message = ujson.loads(msg)
    for reg_topic in Rule.actions_list.keys():
        regex = ure.compile(reg_topic)
        if regex.match(topic.decode("utf-8")):
            if not isinstance(Rule.actions_list[reg_topic], list):
                loop.create_task(Rule.actions_list[reg_topic].process_event(message, client_pub))

            else:
                for action in Rule.actions_list[reg_topic]:
                    loop.create_task(action.process_event(message, client_pub))

if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()
    loop.close()
