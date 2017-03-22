
from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio
import time as Time

class Action:

    def __init__(self, out_topic, func_type, _filter=None, aggregator=None, window=None, converter=None):

        self.out_topic = out_topic
        self.func_type = func_type
        self._filter = _filter
        self.aggregator = aggregator
        self.window = window
        self.converter = converter

        self.in_window = False #Flag sinalizing if there is a window in action
        self.window_values = None #variable to hold window values

    async def process_event(self, message, client):
        value = message.get("event").get("payloadData").get("value")
        device = message.get("event").get("payloadData").get("device")

        if self._filter != None and not self._filter.evaluate(value):
            return

        if self.window != None and self.aggregator != None:

            if self.window._type == 'time':
                if self.aggregator._type == 'any':
                    if value is 0:
                        return

                    event_id = Devices.new_event(self)
                    data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
                    client.publish(self.out_topic, str.encode(data))

                    await asyncio.sleep(self.window.value)

                    if Devices.devices[self] == event_id:
                        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'
                        client.publish(self.out_topic, str.encode(data))

                elif self.aggregator._type == 'avg':

                    pass #TODO
                else: #None
                    pass #TODO

            elif self.window._type == 'length':
                if self.aggregator._type == 'any':
                    pass

                elif self.aggregator._type == 'avg':
                    if not in_window:
                        in_window = True


                else: #None
                    pass #TODO

        if self.converter != None:

            if self.converter._type == 'lux_to_percentage':

                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(( 100 -(value * (100/self.converter.max_lux))))) + '}}}'

                yield client.publish(self.out_topic, str.encode(data))
            elif self.converter._type == 'set_to_1':
                pass
            elif self.converter._type == 'set_to_0':
                pass
