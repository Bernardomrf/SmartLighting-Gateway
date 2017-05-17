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

    loop.create_task(wait_message())
    loop.create_task(heart_beat())

    yield from asyncio.sleep(0)


@asyncio.coroutine
def wait_message():
    while True:
        client.check_msg()
        yield from asyncio.sleep(0) #Needed to check heart beat (0 or 0.001)


@asyncio.coroutine
def heart_beat():
    while True:
        global enable

        data = '{"gateway":"'+confs.GATEWAY_NAME+'"}'
        client_pub.publish('/SM/hb/', str.encode(data))

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

    if topic.decode("utf-8") == '/SM/add_rule':
        print('entrei')
        RuleLoader.process_rules(msg)
        return
    if topic.decode("utf-8") == '/SM/remove_rule':

        rule_id = msg.decode("utf-8")
        #print(Rule.actions_list)
        for reg_topic in Rule.actions_list:
            for i, (r_id, action) in enumerate(Rule.actions_list[reg_topic]):
                if r_id == rule_id:
                    del Rule.actions_list[reg_topic][i]
                    if len(Rule.actions_list[reg_topic]) is 0:
                        del Rule.actions_list[reg_topic]
        #print(Rule.actions_list)
        return

    if not enable:
        return

    if topic.decode("utf-8") == '/SM/add_device' or topic.decode("utf-8") == '/SM/delete_device':
        return
    '''if(gc.mem_alloc()>confs.MAX_MEM):
        gc.collect()
        print(gc.mem_alloc())'''

    if '/SM/out_events' in topic.decode("utf-8"):
        return

    message = ujson.loads(msg)
    for reg_topic in Rule.actions_list.keys():
        regex = ure.compile(reg_topic)
        if regex.match(topic.decode("utf-8")):
            #print('applying rule')
            if not isinstance(Rule.actions_list[reg_topic], list):
                loop.create_task(Rule.actions_list[reg_topic][1].process_event(message, client_pub))

            else:
                for (r_id, action) in Rule.actions_list[reg_topic]:
                    loop.create_task(action.process_event(message, client_pub))

if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()
    loop.close()
