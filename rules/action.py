
from umqtt.simple import MQTTClient
import configs as confs
from rules.rule import Rule
import uasyncio as asyncio
import utime as time

class Action:

    events = {}
    event_id = 0

    def new_event(action):
        Action.event_id+=1
        Action.events[action] = Action.event_id
        return Action.event_id

    def __init__(self, out_topic, func_type, _filter=None, aggregator=None, window=None, converter=None, value_action=None, percent_if_true=None, percent_if_false=None):

        self.out_topic = out_topic
        self.func_type = func_type
        self._filter = _filter
        self.aggregator = aggregator
        self.window = window
        self.converter = converter
        self.value_action = value_action
        self.percent_if_true = percent_if_true
        self.percent_if_false = percent_if_false

        self.bool_value = None
        self.in_window = False #Flag sinalizing if there is a window in action
        self.window_values = [] #variable to hold window values

    async def process_event(self, message, client, r_id, enable):
        value = message.get("event").get("payloadData").get("value")

        if self._filter != None and not self._filter.evaluate(value):
            return

        if self.window != None and self.aggregator != None:

            if self.window._type == 'time':
                if self.aggregator._type == 'any':
                    if value is 0:
                        return

                    event_id = Action.new_event(self)

                    Action.apply_converter(self, value, client,r_id, enable)

                    # Apply Time window
                    #tm = time.time()
                    await asyncio.sleep(self.window.value)
                    #print(time.time()-tm)
                    if Action.events[self] == event_id:
                        Action.apply_converter(self, 0, client, r_id, enable)

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
                            Action.apply_converter(self,average,client,r_id, enable)
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

                        Action.apply_converter(self,average,client,r_id, enable)
                    else:
                        self.window_values.append(value)
                        return

                else: #None
                    if len(self.window_values) == self.window.value:
                        del self.window_values[0]
                        self.window_values.append(value)

                        if all(i==0 for i in self.window_values):
                            Action.apply_converter(self,average,client,r_id, enable)
                        else:
                            return
                    else:
                        self.window_values.append(value)
                        return

        else:
            Action.apply_converter(self,value,client, r_id, enable)

    def apply_converter(self,value,client,r_id, enable):

        if self.func_type == 'setif_value_percent' and self.value_action != None:
            #print(value)
            self.value_action.bool_value = eval(str(value))
            return

        if self.converter != None:

            if self.converter._type == 'lux_to_percentage':
                lux = int(( 100 -(value * (100/self.converter.max_lux))))
                if self.bool_value is 0 and self.bool_value is not None:
                    lux = lux * (self.percent_if_false/100)
                elif self.bool_value is not 0 and self.bool_value is not None:
                    lux = lux * (self.percent_if_true/100)

                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(lux)) + '}}}'
                Action.send_gateways(data, self.out_topic, r_id, enable, client)
                #client.publish(self.out_topic, str.encode(data))

            elif self.converter._type == 'set_to_1':
                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":1}}}'
                Action.send_gateways(data, self.out_topic, r_id, enable, client)
                #client.publish(self.out_topic, str.encode(data))

            elif self.converter._type == 'set_to_0':
                data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":0}}}'
                Action.send_gateways(data, self.out_topic, r_id, enable, client)
                #client.publish(self.out_topic, str.encode(data))
        else:

            if self.bool_value == False:
                value = value * (self.percent_if_false/100)
            elif self.bool_value == True:
                value = value * (self.percent_if_true/100)
            data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(value)) + '}}}'
            Action.send_gateways(data, self.out_topic, r_id, enable, client)
            #client.publish(self.out_topic, str.encode(data))

    def send_gateways(data, out_topic, r_id, enable, client):

        if enable:
            client.publish(out_topic, str.encode(data))
        else:
            for gw in Rule.output_topics_per_gw[r_id]:
                gw_client = MQTTClient("pub_output", gw)
                gw_client.connect()
                gw_client.publish(out_topic, str.encode(data))
                gw_client.disconnect()

