# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import time
import configs as confs
import random
from threading import Thread, Event
import atexit

devices = []

class RandomGenerator(Thread):
    global devices
    def __init__(self, device):
        super(RandomGenerator, self).__init__()
        self._stop_event = Event()
        self._device = device


    def run(self):

        while True:
            #print (devices)
            #mqttc.publish(confs.DEVICES_MOTION[self._device], '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')
            #print(self._device)
            #print(devices[0])
            if self._device in devices:
                #print('it is')
                publish.single(confs.DEVICES_MOTION[self._device], payload='{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}', qos=0, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)

                time.sleep(1)
                publish.single(confs.DEVICES_MOTION[self._device], payload='{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}', qos=0, retain=False,
                                    hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                    will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)

                self._stop_event.wait(random.randint(2, 12))
            else:
                time.sleep(5)


    def stop(self):

        self._stop_event.set()

def subscribe():
    import paho.mqtt.subscribe as subscribe
    subscribe.callback(on_message, ["/SM/delete_device", "/SM/add_device"], hostname="localhost")

def on_message(client, userdata, msg):
    print(msg.payload)
    if msg.topic == '/SM/add_device':
        devices.append(msg.payload.decode("utf-8"))
        #print(devices)
    elif msg.topic == '/SM/delete_device':
        print('remove')
        if(msg.payload.decode("utf-8") in devices):
            devices.remove(msg.payload.decode("utf-8"))


def main():
    t = Thread(target=subscribe)

    t.start()
    print('aqui')
    for i in range(1,76):


        publish.single("/SM/devconfig", payload='{"device": {"device_id": "light_c'+str(i)+'"}, "objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 1501, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}]}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)
        publish.single("/SM/regdevice", payload='{"device":"light_c'+str(i)+'", "gateway":"sonata9"}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)

        time.sleep(0.1)

    for i in range(1,109):
        publish.single("/SM/devconfig", payload='{"device": {"device_id": "light'+str(i)+'"}, "objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 1501, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}]}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)
        publish.single("/SM/regdevice", payload='{"device":"light'+str(i)+'", "gateway":"sonata9"}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)

        time.sleep(0.1)

    for i in range(1,165):

        publish.single("/SM/devconfig", payload='{"objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 3302, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 5500}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}], "device": {"device_id": "motion'+ str(i) +'"}}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)
        publish.single("/SM/regdevice", payload='{"device":"motion' + str(i) + '", "gateway":"sonata9"}', qos=1, retain=False,
                                hostname="sonata4.local", port=1883, client_id="", keepalive=60,
                                will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)

        time.sleep(0.1)
        RandomGenerator("motion" + str(i)).start()


    print('aqui')

if __name__ == '__main__':
    main()


@atexit.register
def goodbye():
    #print(topics_list)
    print(devices)

# time.sleep(5)

# print mqttc.publish("sonoff1/gpio/12", "0")
# mqttc.loop()


#mqttc.publish("/SM/devconfig", '{"objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 3302, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 5500}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}], "device": {"device_id": "motion'+ str(i) +'"}}')mqttc.publish("/SM/regdevice", '{"device":"motion' + str(i) + '", "gateway":"gateway-pi"}')

#mqttc.publish("/SM/devconfig", '{"device": {"device_id": "'+light+'"}, "objects": [{"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}], "object_id": 3}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}], "object_id": 1}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}], "object_id": 1501}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}], "object_id": 1301}]}')mqttc.publish("/SM/regdevice", '{"device":"'+light+'", "gateway":"gateway-pi"}')




#for light in confs.DECICES_LIGHT:
#mqttc.publish("/SM/devconfig", '{"device": {"device_id": "'+light+'"}, "objects": [{"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}], "object_id": 3}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}], "object_id": 1}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}], "object_id": 1501}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}], "object_id": 1301}]}')

#mqttc.publish("/SM/regdevice", '{"device":"'+light+'", "gateway":"gateway-pi"}')
#time.sleep(0.05)'''



#while 1:
    #time.sleep(2)
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')
    #print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_9/1/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')

    #time.sleep(15)
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')
    #print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_9/1/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')

    #time.sleep(10)'''
