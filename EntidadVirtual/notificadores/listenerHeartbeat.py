import paho.mqtt.client as paho
from datetime import timedelta
from datetime import datetime
import time
import threading


delta = timedelta(seconds=10)
ahora = datetime.now()
index = 0
contador = 0
heartbeat = "I'm alive"
salida = True
inicioHilo = False
mensaje = ""
topico_yale = "conjunto1/residencia1/heartbeathub"


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client,userdata,mid):
    print("mid: "+str(mid))

def sent_heartbeat():
    ahoraheart =datetime
    while True:
        while ahoraheart + delta > datetime.now():
            time.sleep(1)
        print("Hub alive")
        client.publish(topico_yale,"Hub alive")
        ahora = datetime.now()


def listen_heartbeat():
    global salida, ahora, index, mensaje, contador
    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(mensaje)

    while salida:
        while ahora + delta > datetime.now():
            print(index)
            index = index + 1
            time.sleep(1)

            if "alive" in mensaje:
                contador = 0
                ahora = datetime.now()
                mensaje = ""

        contador += 1
        print(contador)
        if contador >= 3:
            print("chucu chucu chucu")
            client.publish(topico_yale, "chucu chucu")
            salida = False

        ahora = datetime.now()


hilo = threading.Thread(target=listen_heartbeat())
hiloheart = threading.Thread(target=sent_heartbeat())
hiloheart.start()

def on_message(client, userdata, msg):
    global inicioHilo, mensaje
    if not inicioHilo:
        hilo.start()
        inicioHilo = True
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    mensaje = str(msg.payload)








client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("conjunto1/residencia1/alerta")
client.loop_forever()



