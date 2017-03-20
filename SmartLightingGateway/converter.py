from umqtt.simple import MQTTClient
import configs as confs
import uasyncio as asyncio


class Converter:

    def get_converter(c_type, max_lux=None):
        if c_type is 'lux_to_percentage':
            return LuxToPercent(max_lux)
        elif c_type is 'set_to_1':
            return SetTo1()
        elif c_type is 'set_to_0':
            return SetTo0()
        else:
            return None

    def do_work(out_topic, value, client):

        #3.33333 100/self.max_lux
        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(( 100 -(value * 3.333333)))) + '}}}'

        yield client.publish(out_topic, str.encode(data))

    def name(self):
        return "Converter"


class LuxToPercent(Converter):

    c_type = 'lux_to_percentage'

    def __init__(self, max_lux):
        self.max_lux = max_lux

	def get_dict(self):
		d = dict()
		d['type'] = LuxToPercent.c_type
		d['max_lux'] = self.max_lux
		return d


class SetTo1(Converter):
	c_type = 'set_to_1'

	def get_dict(self):
		d = dict()
		d['type'] = SetTo1.c_type
		return d


class SetTo0(Converter):
	c_type = 'set_to_0'

	def get_dict(self):
		d = dict()
		d['type'] = SetTo0.c_type
		return d
