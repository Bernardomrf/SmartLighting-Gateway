# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import configs as confs
import random
from threading import Thread, Event

mqttc = mqtt.Client()
#mqttc.username_pw_set("server", password="fire")
mqttc.connect("sonata4.local", 1883)

class RandomGenerator(Thread):
    def __init__(self, device, mqttc):
        super(RandomGenerator, self).__init__()
        self._stop_event = Event()
        self._mqttc = mqttc
        self._device = device

    def run(self):

        while True:

            mqttc.publish(confs.DEVICES_MOTION[self._device], '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')


            time.sleep(1)
            mqttc.publish(confs.DEVICES_MOTION[self._device], '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')

            self._stop_event.wait(random.randint(2, 12))


    def stop(self):

        self._stop_event.set()


for light in confs.DECICES_LIGHTC:
    mqttc.publish("/SM/devconfig", '{"device": {"device_id": "'+light+'"}, "objects": [{"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}], "object_id": 3}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}], "object_id": 1}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}], "object_id": 1501}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}], "object_id": 1301}]}')

    mqttc.publish("/SM/regdevice", '{"device":"'+light+'", "gateway":"gateway-pi"}')
    time.sleep(0.05)

'''for light in confs.DECICES_LIGHT:
    mqttc.publish("/SM/devconfig", '{"device": {"device_id": "'+light+'"}, "objects": [{"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}], "object_id": 3}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}], "object_id": 1}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}], "object_id": 1501}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}], "object_id": 1301}]}')

    mqttc.publish("/SM/regdevice", '{"device":"'+light+'", "gateway":"gateway-pi"}')
    time.sleep(0.05)'''

for i in range(1,165):
    mqttc.publish("/SM/devconfig", '{"objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 3302, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 5500}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}], "device": {"device_id": "motion'+ str(i) +'"}}')
    mqttc.publish("/SM/regdevice", '{"device":"motion' + str(i) + '", "gateway":"gateway-pi"}')
    time.sleep(0.05)
    RandomGenerator("motion" + str(i), mqttc).start()

'''while 1:
    #time.sleep(2)
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')
    print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_9/1/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')

    time.sleep(15)
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')
    print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_9/1/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')

    time.sleep(10)'''



mqttc.loop()


# time.sleep(5)

# print mqttc.publish("sonoff1/gpio/12", "0")
# mqttc.loop()
