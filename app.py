import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("forge/test")

def on_message(client, userdata, msg):
    print(client, msg.topic+" "+str(msg.payload))
    print(client.__dict__)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

