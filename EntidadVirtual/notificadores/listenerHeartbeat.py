import paho.mqtt.client as paho
from datetime import timedelta
from datetime import datetime
import time


delta = timedelta(seconds=10)
ahora = datetime.now()
index = 0
contador = 0
heartbeat = "I'm alive"
salida = True


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client,userdata,mid):
    print("mid: "+str(mid))



def on_message(client, userdata, msg):

    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(str(msg.payload))

    while salida:
        while ahora + delta > datetime.now():
            print(index)
            index = index + 1
            time.sleep(1)

            if "alive" in msg.payload:
                contador = 0
                ahora = datetime.now()

        contador += 1
        print(contador)
        if contador >= 3:
            print("chucu chucu chucu")
            salida = False

        ahora = datetime.now()






client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("conjunto1/residencia1/alerta")
client.loop_forever()



