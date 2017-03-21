from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio
import time as Time

class Window:

    def get_window(_type, value, units=None):
        if _type == 'length':
            return LengthWindow(value)
        elif _type == 'time':
            return TimeWindow(value, units)
        else:
            return None


    def name(self):
        return "Window"


class LengthWindow(Window):

    _type = 'length'

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

    _type = 'time'

    def __str__(self):
        return 'Time Window of %d %s'%(self.value, self.units)

    def __init__(self, value, units):
        self.value = value
        self.units = units

	def get_dict(self):
		d = dict()
		d['type'] = TimeWindow._type
		d['value'] = self.value
		d['units'] = self.units
		return d
