import paho.mqtt.client as paho
import datetime


espera =datetime.time
contador=0


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client,userdata,mid):
    print("mid: "+str(mid))



def on_message(client, userdata, msg):

    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(str(msg.payload))

    if espera

    if "alive" in msg.payload:
        espera = datetime.time
        print("Se hizo sustring")
        contador =0




    if(contador>=3)






client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("conjunto1/residencia1/alerta")
client.loop_forever()



