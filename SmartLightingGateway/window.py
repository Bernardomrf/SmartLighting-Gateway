from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio
import time as Time

class Window:

    def get_window(w_type, value, units=None):
        if w_type is 'length':
            return LengthWindow(value)
        elif w_type is 'time':
            return TimeWindow(value, units)
        else:
            return None

    async def do_work(out_topic, value, device, time, client):

        if value is 0:
            return

        event_id = Devices.new_event(device)

        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
        client.publish(out_topic, str.encode(data))

        await asyncio.sleep(time)

        if Devices.devices[device] is event_id:
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'
            client.publish(out_topic, str.encode(data))

    def name(self):
        return "Window"


class LengthWindow(Window):

    w_type = 'length'

    def __init__(self, value):
        self.value = value

    def __str__(self):
		return 'Length Window'

    def get_dict(self):
		d = dict()
		d['type'] = LengthWindow._type
		d['value'] = self.value
		return d

class TimeWindow(Window):

    w_type = 'time'

    def __str__(self):
        return 'Time Window of %d %s'%(self.value, self.units)

    def __init__(self, value, units):
        self.value = value
        self.units = units

	def get_dict(self):
		d = dict()
		d['type'] = TimeWindow.w_type
		d['value'] = self.value
		d['units'] = self.units
		return d
