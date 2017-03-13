import time
import sys
import ubinascii
import ujson
import ure
import uasyncio as asyncio
import configs as confs

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

    client.subscribe(confs.SUB_TOPIC)

    loop.run_until_complete(wait_message())


async def wait_message():
    while True:
        client.wait_msg()
        await asyncio.sleep(0)


async def do_work(topic, message, event_id):
    global devices

    value = message.get("event").get("payloadData").get("value")
    if value is 0:
        return
    devices[message.get("event").get("payloadData").get("device")] = event_id

    regex = ure.compile('/SM/in_events/IT2/floor_0/Sala/1/1/[^/]+/3302/[^/]+/5500/[^/]+')
    regex2 = ure.compile('/SM/in_events/IT2/floor_0/Sala/1/2/[^/]+/3302/[^/]+/5500/[^/]+')

    data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value)
    final_data = data + '}}}'
    if(regex.match(topic.decode("utf-8"))):
        print(str.encode(final_data))
        out_topic = "/SM/out_events/IT2/floor_0/Sala/1/1/all/1501/all/15011/all"
        client.publish(out_topic, str.encode(final_data))

        await asyncio.sleep(6)
        if devices[message.get("event").get("payloadData").get("device")] is event_id:

            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0)
            final_data = data + '}}}'
            client.publish(out_topic, str.encode(final_data))

    if(regex2.match(topic.decode("utf-8"))):
        print(str.encode(final_data))
        out_topic = "/SM/out_events/IT2/floor_0/Sala/1/2/all/1501/all/15011/all"
        client.publish(out_topic, str.encode(final_data))

        await asyncio.sleep(6)
        if devices[message.get("event").get("payloadData").get("device")] is event_id:

            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0)
            final_data = data + '}}}'
            client.publish(out_topic, str.encode(final_data))

    print('message arrive')

def message_arrive(topic, msg):
    global event_id
    message = ujson.loads(msg)
    event_id+=1
    loop.create_task(do_work(topic, message, event_id))

if __name__ == '__main__':
    main()
