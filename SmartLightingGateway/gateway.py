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
from rule_loader import RuleLoader
from umqtt.simple import MQTTClient

client = MQTTClient(confs.CLIENT_ID, confs.HOST)
loop = asyncio.get_event_loop()
devices = {}
event_id = 0
enable = False

async def main():
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

    client.subscribe(confs.SUB_TOPIC)
    loop.create_task(wait_message())



async def wait_message():
    while True:
        client.wait_msg()
        await asyncio.sleep(0.001)


def message_arrive(topic, msg):
    if not enable:
        print('ignored')
        return

    if(gc.mem_alloc()>1000000):
        gc.collect()
        print(gc.mem_alloc())

    message = ujson.loads(msg)
    for reg_topic in Rules.actions_list.keys():
        regex = ure.compile(reg_topic)
        if regex.match(topic.decode("utf-8")):
            if not isinstance(Rules.actions_list[reg_topic], list):
                loop.create_task(Rules.actions_list[reg_topic].process_event(message, client))

            else:
                for action in Rules.actions_list[reg_topic]:
                    loop.create_task(action.process_event(message, client))


@asyncio.coroutine
def serve(reader, writer):
    yield from reader.read()

    global enable
    enable  = not enable




if __name__ == '__main__':
    loop.create_task(asyncio.start_server(serve, "127.0.0.1", 12000))
    loop.create_task(main())
    loop.run_forever()
    loop.close()
