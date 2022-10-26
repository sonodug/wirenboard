import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# Connection parameters to the MQTT broker
HOST = "192.168.1.16"  # Suitcase IP
PORT = 1883  # Standard connection port for Mosquito
KEEPALIVE = 60  # The waiting time for message delivery, if it is exceeded when sending, the broker will be considered unavailable

# Drivers
SUB_TOPICS = {
    '/devices/power_status/controls/Vin': 'voltage',
    '/devices/wb-msw-v3_21/controls/Sound Level': 'sound',
    '/devices/wb-msw-v3_21/controls/Illuminance': 'illuminance',
}

JSON_LIST = []

JSON_DICT = {}
for value in SUB_TOPICS.values():
    JSON_DICT[value] = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    for topic in SUB_TOPICS.keys():
        client.subscribe(topic)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic

    param_name = SUB_TOPICS[topic]
    JSON_DICT[param_name] = payload
    JSON_DICT['time'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    JSON_LIST.append(JSON_DICT.copy())

    print(f"{topic} {payload} | {str(datetime.now())}")


    with open('data.json', 'w') as file:
        json_string = json.dumps(JSON_LIST)
        file.write(json_string)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, KEEPALIVE)

    client.loop_forever(100000)
    print(JSON_DICT)

if __name__ == "__main__":
    main()
