# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
mqttc = mqtt.Client()
#mqttc.username_pw_set("server", password="fire")
mqttc.connect("sonata4.local", 1883)

for i in range(1,77):
    print mqttc.publish("/SM/devconfig", '{"device": {"device_id": "light_c'+ str(i) +'"}, "objects": [{"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}], "object_id": 3}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}], "object_id": 1}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}], "object_id": 1501}, {"object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}], "object_id": 1301}]}')
    print mqttc.publish("/SM/regdevice", '{"device":"light_c' + str(i) + '", "gateway":"gateway-pi"}')
    time.sleep(0.05)

for i in range(1,165):
    print mqttc.publish("/SM/devconfig", '{"objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 3302, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 5500}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}], "device": {"device_id": "motion'+ str(i) +'"}}')
    print mqttc.publish("/SM/regdevice", '{"device":"motion' + str(i) + '", "gateway":"gateway-pi"}')
    time.sleep(0.05)

while 1:
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')
    print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_5/3/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":1}}}')

    time.sleep(1)
    #print mqttc.publish("/SM/out_events/IT2/Floor0/Corredor/all/all/all/1501/all/all/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')
    print mqttc.publish("/SM/in_events/IT2/Floor0/Corredor/0_13_5/3/all/3302/all/5500/all", '{"event": {"metaData":{"operation":"set"},"payloadData":{"value":0}}}')

    time.sleep(10)



mqttc.loop()

# time.sleep(5)

# print mqttc.publish("sonoff1/gpio/12", "0")
# mqttc.loop()
