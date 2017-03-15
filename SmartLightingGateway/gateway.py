import time
import sys
import ubinascii
import ujson
import gc
import ure
import uasyncio as asyncio
import configs as confs
from rules import Rules
from converter import Converter
from action import Action
from devices import Devices
from window import Window
from umqtt.simple import MQTTClient

client = MQTTClient(confs.CLIENT_ID, confs.HOST)
loop = asyncio.get_event_loop()
devices = {}
event_id = 0

def main():
    client.DEBUG = True
    client.set_callback(message_arrive)

    try:
        client.connect(clean_session=False)
    except Exception:
        print("Error while connecting to mqtt broker")
        sys.exit()

    print("Connected to {}".format(confs.HOST))
    with open('rule.json') as data_file:
        data = ujson.load(data_file)
    with open('rule2.json') as data_file:
        data2 = ujson.load(data_file)

    load_json(data)
    load_json(data2)

    client.subscribe(confs.SUB_TOPIC)

    loop.run_until_complete(wait_message())

async def wait_message():
    while True:
        client.wait_msg()
        await asyncio.sleep(0)

def message_arrive(topic, msg):
    if(gc.mem_alloc()>1000000):
        gc.collect()
    print(gc.mem_alloc())
    message = ujson.loads(msg)
    for reg_topic in Rules.actions_list.keys():
        regex = ure.compile(reg_topic)
        if regex.match(topic.decode("utf-8")):
            if not isinstance(Rules.actions_list[reg_topic], list):


                module = Rules.actions_list[reg_topic].module

                if(module.name() is "Window"):
                    loop.create_task(Window.do_work(Rules.actions_list[reg_topic].out_topic,
                    message.get("event").get("payloadData").get("value"),

                    message.get("event").get("payloadData").get("device"),
                    Rules.actions_list[reg_topic].module.time, client))
                elif(module.name() is "Converter"):
                    #Devices.new_event(message.get("event").get("payloadData").get("device"))

                    loop.create_task(Converter.do_work(Rules.actions_list[reg_topic].out_topic,
                    message.get("event").get("payloadData").get("value"),
                    client))
            else:
                for action in Rules.actions_list[reg_topic]:
                    act = action.module
                    time = act.time
                    loop.create_task(Window.do_work(action.out_topic,
                    message.get("event").get("payloadData").get("value"),

                    message.get("event").get("payloadData").get("device"), time, client))

def load_json(data):
    for subrule in data['subrules']:
        for action in subrule['actions']:
            for listener in action['function']['listen_data']['listeners']:
                if 'window' in action['function']['listen_data']:
                    module = Window(action['function']['listen_data']['window']['type'],
                    action['function']['listen_data']['window']['value'],
                    action['function']['listen_data']['window']['units'])

                elif 'converter' in action['function']['listen_data']:
                    print(action['function']['listen_data']['converter']['max_lux'])
                    module = Converter(action['function']['listen_data']['converter']['type'],
                    action['function']['listen_data']['converter']['max_lux'])


                new_action = Action(listener['topic'],
                '/SM'+action['target']['topic'],
                action['function']['name'],
                module)

                Rules.add_action(new_action, '/SM'+listener['topic'].replace("/+","/[^/]+"))

    print(Rules.actions_list)


if __name__ == '__main__':
    main()
