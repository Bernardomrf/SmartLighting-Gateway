import paho.mqtt.client as MQTTClient
import time
import configs as confs
import sys

client = MQTTClient.Client()


def main():
    client.DEBUG = True



    try:
        client.connect('gateway-pi.local', 1883)
    except Exception:
        print("Error while connecting to mqtt broker")
        sys.exit()
    print("Connected to {}".format(confs.HOST))

    while True:
        print('sending HB')
        data = 'HB'
        client.publish(confs.HB_TOPIC, str.encode(data))
        time.sleep(5)

if __name__ == '__main__':
    main()
