from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio
import time as Time

class Window:

    def __init__(self, wind_type, time, units):
        self.wind_type = wind_type
        self.time = time
        self.units = units

    async def do_work(out_topic, value, device, time, client):

        print(out_topic)
        if value is 0:
            return
        event_id = Devices.new_event(device)

        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'

        client.publish(out_topic, str.encode(data))

        start = Time.time()
        await asyncio.sleep(time)
        end = Time.time()
        
        if Devices.devices[device] is event_id:
            print('desligar')
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'

            client.publish(out_topic, str.encode(data))
        else:
            print('já estava ligada')

        print(end-start)
    def name(self):
        return "Window"
