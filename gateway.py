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
from rules.device_register import DeviceRegister
from umqtt.simple import MQTTClient

client = MQTTClient(confs.CLIENT_ID, confs.HOST)
client_pub = MQTTClient(confs.CLIENT_ID_PUB, confs.HOST_PUB)

loop = asyncio.get_event_loop(1000)
enable = False
last_hb = time.time()
devices_on_control = []

@asyncio.coroutine
def main():


    client.set_callback(message_arrive)
    client_pub.set_callback(event_trigger)
    client.connect()
    client_pub.connect()
    client.subscribe(confs.SUB_TOPIC, qos=1)
    client.subscribe(confs.HB_TOPIC, qos=1)

    loop.create_task(get_message())
    loop.create_task(wait_message())
    loop.create_task(heart_beat())

    yield from asyncio.sleep(0)

@asyncio.coroutine
def get_message():
    while True:
        client_pub.check_msg()
        yield from asyncio.sleep(0) #Needed to check heart beat (0 or 0.001)

@asyncio.coroutine
def wait_message():
    while True:
        client.check_msg()
        yield from asyncio.sleep(0) #Needed to check heart beat (0 or 0.001)


@asyncio.coroutine
def heart_beat():
    while True:
        global enable
        if enable:

            data = '{"gateway":"'+confs.GATEWAY_NAME+'"}'
            client_pub.publish('/SM/hb/', str.encode(data))
            #print(devices_on_control)
            #print(Rule.actions_list.keys())
        if ((time.time() - last_hb) > confs.HB_TIMER):
            print('GatewayCEP - UP')
            enable = True
        else:
            print('GatewayCEP - DOWN')
            enable = False
        yield from asyncio.sleep(confs.HB_TIMER)

def event_trigger(topic, msg):

    if '/SM/out_events' in topic.decode("utf-8"):
        print(topic)
        return

    if '/SM/in_events' in topic.decode("utf-8"):

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

def message_arrive(topic, msg):
    #print(topic)
    if topic.decode("utf-8") == confs.HB_TOPIC:
        global last_hb
        last_hb = time.time()
        return

    if not enable:
        return

    if topic.decode("utf-8") == '/SM/add_rule':
        #print('entrei')
        topics = RuleLoader.process_rules(msg)
        # SUBSCREVER AOS TOPICOS QUE O PROCESS RULE APANHA(IN EVENTS )
        for tpc in topics:
            #print(tpc)
            client_pub.subscribe(tpc, qos=1)

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


    if topic.decode("utf-8") == '/SM/send_devices':
        print('Send Devices')
        DeviceRegister.register(client_pub)
        return

    if topic.decode("utf-8") == '/SM/add_device':
        #print('adding device')
        json_dict = ujson.loads(msg)
        device = list(json_dict.keys())[0]
        topics = json_dict[device]
        for tpc in topics:
            print(tpc)
            client_pub.subscribe(tpc, qos=1)
        devices_on_control.append(device)
        return

    if topic.decode("utf-8") == '/SM/delete_device':
        device = msg.decode("utf-8")
        try:
            del devices_on_control[devices_on_control.index(device)]
        except Exception as e:
            print('Device not found')
        return

    '''if(gc.mem_alloc()>confs.MAX_MEM):
        gc.collect()
        print(gc.mem_alloc())'''





if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()
    loop.close()
