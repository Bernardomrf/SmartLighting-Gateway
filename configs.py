HOST = "127.0.0.1"
HOST_PUB = "sonata4.local"
CLIENT_ID = "gateway2"
CLIENT_ID_PUB = "gateway2_pub"
RULES_FOLDER = "resources/json_rules/"
SUB_TOPIC = '#'
HB_TOPIC = '/heart_beat'
RULES_TOPIC = '/SM/rule'
HB_TIMER = 5
MAX_MEM = 2000000
GATEWAY_NAME = 'gateway-pi2.local'
DEVICE_AC = []
DEVICE_TMP = []
DEVICE_HUM = []
DEVICE_LUX = []
DEVICE_MOTION = []
DEVICE_LIGHT = []
DEVICE_LIGHT_B = []
DEVICE_LIGHT_C = []
DEVICE_LIGHT_S = []


for i in range(77,83):
    DEVICE_LIGHT.append('light%d'%i)

for i in range(73,76):
    DEVICE_MOTION.append('motion%d'%i)

for i in range(72,75):
    DEVICE_LUX.append('lux%d'%i)

"""
for i in range(1,46):
    DEVICES.append('ac%d'%i)

for i in range(1,50):
    DEVICES.append('tmp%d'%i)


for i in range(1,50):
    DEVICES.append('hum%d'%i)


for i in range(1,157):
    DEVICE_LUX.append('lux%d'%i)


for i in range(1,165):
    DEVICE_MOTION.append('motion%d'%i)


for i in range(1,109):
    DEVICE_LIGHT.append('light%d'%i)


for i in range(1,34):
    DEVICES.append('light_b%d'%i)


for i in range(1,10):
    DEVICES.append('light_s%d'%i)


for i in range(1,77):
    DEVICE_LIGHT_C.append('light_c%d'%i)

"""

