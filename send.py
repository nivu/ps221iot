import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish("forge/test","Hello World")
    client.subscribe("forge/test")

def on_message(client, userdata, msg):
    print(client, msg.topic+" "+str(msg.payload))

def on_publish(client,userdata,result):
    print("data published \n")
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish   

client.connect("broker.hivemq.com", 1883, 60)

for i in range(1000):
    ret= client.publish("forge/test",i)
    time.sleep(5)

