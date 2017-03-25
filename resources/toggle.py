import paho.mqtt.client as MQTTClient
import time
import sys

client = MQTTClient.Client()

HOST = 'gateway-pi.local'
PORT = 1883
HB_TOPIC = '/heart_beat'

def main():
    client.DEBUG = True
    try:
        client.connect(HOST, PORT)
    except Exception:
        print("Error while connecting to mqtt broker")
        sys.exit()
    print("Connected to {}".format(HOST))

    while True:
        print('sending HB')
        data = 'HB'
        client.publish(HB_TOPIC, str.encode(data))
        time.sleep(5)

if __name__ == '__main__':
    main()
