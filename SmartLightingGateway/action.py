
from umqtt.simple import MQTTClient
import configs as confs

import uasyncio as asyncio
import time as Time

class Action:

    events = {}
    event_id = 0

    def new_event(action):
        Action.event_id+=1
        Action.events[action] = Action.event_id
        return Action.event_id

    def __init__(self, out_topic, func_type, _filter=None, aggregator=None, window=None, converter=None):

        self.out_topic = out_topic
        self.func_type = func_type
        self._filter = _filter
        self.aggregator = aggregator
        self.window = window
        self.converter = converter

        self.in_window = False #Flag sinalizing if there is a window in action
        self.window_values = [] #variable to hold window values

    async def process_event(self, message, client):
        value = message.get("event").get("payloadData").get("value")

        if self._filter != None and not self._filter.evaluate(value):
            return

        if self.window != None and self.aggregator != None:

            if self.window._type == 'time':
                if self.aggregator._type == 'any':
                    if value is 0:
                        return

                    event_id = Action.new_event(self)

                    Action.apply_converter(self, value, client)

                    # Apply Time window
                    await asyncio.sleep(self.window.value)

                    if Action.events[self] == event_id:
                        Action.apply_converter(self, 0, client)

                elif self.aggregator._type == 'avg':
                    pass #TODO


                else: #None
                    pass #TODO

            elif self.window._type == 'length':
                if self.aggregator._type == 'any':
                    if len(self.window_values) == self.window.value:
                        del self.window_values[0]
                        self.window_values.append(value)

                        if not all(i==0 for i in self.window_values):
                            Action.apply_converter(self,average,client)

                        else:
                            return
                    else:
                        self.window_values.append(value)
                        return

                elif self.aggregator._type == 'avg':
                    if len(self.window_values) == self.window.value:
                        del self.window_values[0]
                        self.window_values.append(value)

                        average = int(sum(self.window_values)/float(len(self.window_values)))

                        Action.apply_converter(self,average,client)
                    else:
                        self.window_values.append(value)
                        return

                else: #None
                    if len(self.window_values) == self.window.value:
                        del self.window_values[0]
                        self.window_values.append(value)

                        if all(i==0 for i in self.window_values):
                            Action.apply_converter(self,average,client)

                        else:
                            return
                    else:
                        self.window_values.append(value)
                        return

        else:
            Action.apply_converter(self,value,client)

    def apply_converter(self,value,client):

        if self.converter != None:

            if self.converter._type == 'lux_to_percentage':
                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(( 100 -(value * (100/self.converter.max_lux))))) + '}}}'
                client.publish(self.out_topic, str.encode(data))

            elif self.converter._type == 'set_to_1':
                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":1}}}'
                client.publish(self.out_topic, str.encode(data))

            elif self.converter._type == 'set_to_0':
                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":0}}}'
                client.publish(self.out_topic, str.encode(data))
        else:
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(value) + '}}}'
            client.publish(self.out_topic, str.encode(data))
