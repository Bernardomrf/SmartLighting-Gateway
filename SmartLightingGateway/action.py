
from umqtt.simple import MQTTClient
import configs as confs
from devices import Devices
import uasyncio as asyncio
import time as Time

class Action:

    def __init__(self, in_topic, out_topic, func_type, _filter=None, aggregator=None, window=None, converter=None):
        self.in_topic = in_topic
        self.out_topic = out_topic
        self.func_type = func_type
        self._filter = _filter
        self.aggregator = aggregator
        self.window = window
        self.converter = converter

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

                    event_id = Devices.new_event(device)
                    data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
                    client.publish(self.out_topic, str.encode(data))

                    await asyncio.sleep(self.window.value)

                    if Devices.devices[device] == event_id:
                        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'
                        client.publish(self.out_topic, str.encode(data))

                elif self.aggregator._type == 'avg':
                    pass #TODO
                else: #None
                    pass #TODO

            elif self.window._type == 'time': #length
                pass #TODO

        if self.converter != None:

            if self.converter._type == 'lux_to_percentage':

                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(( 100 -(value * (100/self.converter.max_lux))))) + '}}}'

                yield client.publish(self.out_topic, str.encode(data))
            elif self.converter._type == 'set_to_1':
                pass
            elif self.converter._type == 'set_to_0':
                pass

        '''if value is 0:
            return

        event_id = Devices.new_event(device)

        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
        client.publish(out_topic, str.encode(data))

        await asyncio.sleep(time)

        if Devices.devices[device] is event_id:
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(0) + '}}}'
            client.publish(out_topic, str.encode(data))'''
