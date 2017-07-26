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
gw_in_events = {}
sensors_list = {}

@asyncio.coroutine
def main():


    client.set_callback(message_arrive)
    client_pub.set_callback(event_trigger)
    client.connect()
    client_pub.connect()
    client.subscribe(confs.SUB_TOPIC, qos=1)
    #client.subscribe(confs.HB_TOPIC, qos=1)
    client_pub.subscribe(confs.IN_TOPICS_TOPIC, qos=1)
    client_pub.subscribe(confs.OUT_TOPICS_TOPIC, qos=1)
    client_pub.subscribe(confs.HB_TOPIC, qos=1)

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
        print(gw_in_events)
        print(sensors_list)
        if enable:

            data = '{"gateway":"'+confs.GATEWAY_NAME+'"}'
            client_pub.publish('/SM/hb/', str.encode(data))
            #print(devices_on_control)
            #print(Rule.actions_list.keys())
        if ((time.time() - last_hb) > confs.HB_TIMER):
            print('GatewayCEP - DOWN')
            enable = False
        else:
            print('GatewayCEP - UP')
            enable = True
        yield from asyncio.sleep(confs.HB_TIMER)

def event_trigger(topic, msg):
    global gw_in_events
    global enable

    ################ SEGUNDO CENARIO ###########
    if topic.decode("utf-8") == confs.HB_TOPIC:
        global last_hb
        print("HB2")
        last_hb = time.time()
        return

    if not enable:
        return

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
                    loop.create_task(Rule.actions_list[reg_topic][1].process_event(message, client_pub, Rule.actions_list[reg_topic][0], enable))

                else:
                    for (r_id, action) in Rule.actions_list[reg_topic]:
                        loop.create_task(action.process_event(message, client_pub, r_id, enable))


    if '/gateways/in_topics' in topic.decode("utf-8"):
        gw_in_events = ujson.loads(msg)

    if '/gateways/out_topics' in topic.decode("utf-8"):
        Rule.output_topics_per_gw = ujson.loads(msg)


def message_arrive(topic, msg):
    """if topic.decode("utf-8") == confs.HB_TOPIC:
                    global last_hb
                    print("HB1")
                    last_hb = time.time()
                    return"""

    if not enable:
        global gw_in_events
        global sensors_list
        #TERCEIRO CENARIO

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
                        loop.create_task(Rule.actions_list[reg_topic][1].process_event(message, client_pub, Rule.actions_list[reg_topic][0], enable))

                    else:
                        for (r_id, action) in Rule.actions_list[reg_topic]:
                            loop.create_task(action.process_event(message, client_pub, r_id, enable))

        return
############################################################################################
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

    if topic.decode("utf-8") == '/SM/add_device_sensor':
        #print('adding device')
        json_dict = ujson.loads(msg)
        device = list(json_dict.keys())[0]
        topic = json_dict[device]
        sensors_list[device] = topic
        if device not in devices_on_control:
            devices_on_control.append(device)
        return

    if topic.decode("utf-8") == '/SM/add_device':
        #print('adding device')
        json_dict = ujson.loads(msg)
        device = list(json_dict.keys())[0]
        topics = json_dict[device]
        for tpc in topics:
            print(tpc)
            client_pub.subscribe(tpc, qos=1)
        if device not in devices_on_control:
            devices_on_control.append(device)
        return

    if topic.decode("utf-8") == '/SM/delete_device':
        print('delete')
        device = msg.decode("utf-8")
        try:
            del devices_on_control[devices_on_control.index(device)]
            del sensors_list[sensors_list.index(device)]
        except Exception as e:
            print('Device not found')
        return


    '''if(gc.mem_alloc()>confs.MAX_MEM):
        gc.collect()
        print(gc.mem_alloc())'''

@asyncio.coroutine
def simulate_in_events():

    while True:
        if not enable:
            global sensors_list

            for device, topic in sensors_list.items():
                if 'motion' in device:
                    in_topic = topic + '/3302/0/5500/0'
                    data = '{"event": {"payloadData": {"value": 1, "object_instance": 0, "resource_instance": 0, "object": 3302, "device": "motion125", "resource": 5500}}}'

                elif 'lux' in device:
                    in_topic = topic + '/3301/0/5700/0'
                    data = '{"event": {"payloadData": {"value": 6.95, "object_instance": 0, "resource_instance": 0, "object": 3301, "device": "lux38", "resource": 5700}}}'

                send_in_event(in_topic, data)
                yield from asyncio.sleep(2)
        yield from asyncio.sleep(0.5)
    """/SM/in_events/IT2/Floor0/Corredor/0_13_3/3/motion125/3302/0/5500/0
                b'{"event": {"payloadData": {"value": 1, "object_instance": 0, "resource_instance": 0, "object": 3302, "device": "motion125", "resource": 5500}}}'
                /SM/in_events/IT2/Floor0/Outro/0_6_2/2/lux38/3301/0/5700/0
                b'{"event": {"payloadData": {"value": 6.95, "object_instance": 0, "resource_instance": 0, "object": 3301, "device": "lux38", "resource": 5700}}}'"""


def send_in_event(topic, data):
    global gw_in_events


def compare_topics(in_topic, rule_topic):

    in_topic = in_topic.split('/')
    rule_topic = rule_topic.split('/')

    for i, txt in enumerate(rule_topic):
        try:
            if txt == '+':
                return True

            elif txt != in_topic[i]:
                return False

        except Exception as e:
            return True

    return True

if __name__ == '__main__':
    loop.create_task(main())
    loop.run_forever()
    loop.close()
