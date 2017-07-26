
from umqtt.simple import MQTTClient
import configs as confs

class DeviceRegister:

    def register(client):

        for device in confs.DEVICE_MOTION:
            data ='{"objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 3302, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 5500}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}], "device": {"device_id": "'+ device +'"}}'
            client.publish('/SM/devconfig', str.encode(data))

            data = '{"device":"' + device + '", "gateway":"gateway-pi"}'
            client.publish('/SM/regdevice', str.encode(data))

        """for device in confs.DEVICE_LIGHT_C:
            data ='{"device": {"device_id": "'+ device +'"}, "objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 1501, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}]}'
            client.publish('/SM/devconfig', str.encode(data))

            data = '{"device":"' + device + '", "gateway":"gateway-pi"}'
            client.publish('/SM/regdevice', str.encode(data))
"""
        for device in confs.DEVICE_LIGHT:
            data ='{"device": {"device_id": "'+device+'"}, "objects": [{"object_id": 3, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 11}, {"resource_instance": 0, "resource_id": 16}, {"resource_instance": 0, "resource_id": 4}]}, {"object_id": 1, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 1}, {"resource_instance": 0, "resource_id": 8}, {"resource_instance": 0, "resource_id": 7}, {"resource_instance": 0, "resource_id": 6}, {"resource_instance": 0, "resource_id": 0}]}, {"object_id": 1501, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 15011}, {"resource_instance": 0, "resource_id": 15014}, {"resource_instance": 0, "resource_id": 15013}, {"resource_instance": 0, "resource_id": 15012}]}, {"object_id": 1301, "object_instance": 0, "resources": [{"resource_instance": 0, "resource_id": 13011}, {"resource_instance": 0, "resource_id": 13015}, {"resource_instance": 0, "resource_id": 13014}, {"resource_instance": 0, "resource_id": 13013}, {"resource_instance": 0, "resource_id": 13012}]}]}'
            client.publish('/SM/devconfig', str.encode(data))
            data = '{"device":"' + device + '", "gateway":"gateway-pi"}'
            client.publish('/SM/regdevice', str.encode(data))

        for device in confs.DEVICE_LUX:
            data ='{"device": {"device_id": "'+device+'"}, "objects": [{"resources": [{"resource_id": 11, "resource_instance": 0}, {"resource_id": 16, "resource_instance": 0}, {"resource_id": 4, "resource_instance": 0}], "object_instance": 0, "object_id": 3}, {"resources": [{"resource_id": 1, "resource_instance": 0}, {"resource_id": 8, "resource_instance": 0}, {"resource_id": 7, "resource_instance": 0}, {"resource_id": 6, "resource_instance": 0}, {"resource_id": 0, "resource_instance": 0}], "object_instance": 0, "object_id": 1}, {"resources": [{"resource_id": 5700, "resource_instance": 0}], "object_instance": 0, "object_id": 3301}, {"resources": [{"resource_id": 13011, "resource_instance": 0}, {"resource_id": 13015, "resource_instance": 0}, {"resource_id": 13014, "resource_instance": 0}, {"resource_id": 13013, "resource_instance": 0}, {"resource_id": 13012, "resource_instance": 0}], "object_instance": 0, "object_id": 1301}]}'
            client.publish('/SM/devconfig', str.encode(data))

            data = '{"device":"' + device + '", "gateway":"gateway-pi"}'
            client.publish('/SM/regdevice', str.encode(data))
        ### DO THE REST


