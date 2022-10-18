import paho.mqtt.client as mqtt
import base64
from time import sleep 

# define static variable
# broker = "localhost" # for local connection
broker = "broker.hivemq.com"  # for online version
port = 1883
timeout = 60

username = 'campuspedia'
password = 'qlue'
topic = "teslagrandson/image"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
def on_publish(client,userdata,result):
	print("data published \n")
	


client1 = mqtt.Client("ninno1")
client1.username_pw_set(username=username,password=password)
client1.on_connect = on_connect
client1.on_publish = on_publish
client1.connect(broker,port,timeout)

# client = mqtt.Client("ninno")
# client.connect('broker.hivemq.com')
# client.subscribe("topic")
def send_mqtt(base64_message):


    count = 0
    while count < 1:
    
# client.publish('teslagrandson/image', base64_message)
        client1.publish(topic,payload=base64_message)
        sleep(1)
        count = count + 1