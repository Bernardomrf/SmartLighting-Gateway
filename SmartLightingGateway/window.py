from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio

class Window:

    def __init__(self, wind_type, time, units):
        self.wind_type = wind_type
        self.time = time
        self.units = units

    async def do_work(out_topic, value, event_id, device, time, client):

        if value is 0:
            return

        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'

        client.publish(out_topic, str.encode(data))

        await asyncio.sleep(time)

        if Devices.devices[device] is event_id:
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'

            client.publish(out_topic, str.encode(data))
