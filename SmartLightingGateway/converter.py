from umqtt.simple import MQTTClient
import configs as confs
import uasyncio as asyncio


class Converter:

    def __init__(self, conv_type, value):
        self.conv_type = conv_type
        self.value = value

    def do_work(out_topic, value, client):


        data = '{"event":{"metaData":{"operation":"set"},"payloadData":{"value":' + str(int(( 100 -(value * 3.333333)))) + '}}}'

        yield client.publish(out_topic, str.encode(data))




    def name(self):
        return "Converter"

#( ( 100 -(value * 3.333333) )
