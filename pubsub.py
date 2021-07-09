import paho.mqtt.client as mqtt
import sys
import random
from helper import ConfigLoader
import time
import os

config_obj = ConfigLoader(
	config_path = "config/config.json"
	)
	
config = config_obj.load()

topic = config['topic']
brocker = config['brocker']
username = config['username']
password = config['password']
alias = config['device_id']
port = config['port']

client = mqtt.Client(alias)

json_payload_digital_sensor = "{\"props\": [{\"name\": \"sensor\",value:" + str(random.randint(0,1)) + ",\"type\": \"request\"}]}"
json_payload_custom_payload_sensor = "{\"props\": [{\"name\": \"sensor\",\"value\:" + config["custom_payload"] + ",\"type\": \"request\"}]}"


def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Connected to: " + "broker.shiftr.io")
    else:
        print("Error")


def on_disconnet(client, userdata, flags, rc=0):
    print("Disconnecte with code" + str(rc))



def on_message_from_server(client, userdata, message):
    print("Message Recieved from Server: " + message.payload.decode())



def pub_sub_client():
    try:
        print(" ")
        x = input("Enter value")
        json_payload_analog_sensor = "{\"props\": [{\"name\": \"sensor\",\"value\":" + str(x) + ",\"type\": \"request\"}]}"
        client.publish(topic, payload=json_payload_analog_sensor, qos=1, retain=False)
        print("to exit press Ctrl^C")
        #time.sleep(5)
    except Exception as e:
        client.loop_stop()
        client.disconnect()
        print(e)
        sys.exit(1)


def main():
    try:
        os.system("clear")
        print("Config")
        client.on_connect = on_connect
        client.on_disconnect = on_disconnet

        print("Connecting to brocker...")
        client.username_pw_set(username, password)
        client.connect(brocker, port)
        client.subscribe(topic, qos=1)
        client.loop()
        client.loop_start()
        client.message_callback_add(topic, on_message_from_server)
        print("Device emulator started")
        while (1):
            pub_sub_client()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()