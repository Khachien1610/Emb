import uuid
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO
from gpiozero import Servo
from mfrc522 import SimpleMFRC522
import time
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def Servo_init():
     servo = Servo(22)
     servo.min()


host = 'broker.emqx.io'
port = 1883
clientId = f'python_{str(uuid.uuid4())}'
topic = "/mqtt/servo"
username = 'emqx'
password = 'public'
SERIAL = '62f3b405-5ee7-426e-a922-7eeb33d42f88'
ROOMS = {
    '101': '22'
}
CONFIG = {
    'serial': SERIAL,
    'rooms': list(ROOMS.keys()),
    'floor': '1'
}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def connect_mqtt():
    client = mqtt_client.Client(clientId)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)
    return client


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if 'active' in data:
        if data['serial'] == SERIAL:
            room = data['room']
            foot = ROOMS[room]
            if foot and data['active'] == True:
                servo = Servo(foot)
                servo.max()
                time.sleep(0.5)
                print('On')
            if foot and data['active'] == False:
                servo = Servo(foot)
                servo.min()
                time.sleep(0.5)
                print('Off')


def subscribe(client: mqtt_client):
    client.subscribe(topic)
    print(f'Subscribe to topic`{topic}`')
    client.publish(topic, json.dumps(CONFIG))
    client.on_message = on_message


def mqtt_start():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    Servo_init()
    mqtt_start()
