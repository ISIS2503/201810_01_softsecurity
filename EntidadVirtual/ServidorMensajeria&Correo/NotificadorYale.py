#!/usr/bin/env python3
from email.mime.text import MIMEText
import paho.mqtt.client as mqtt_connect
import smtplib
import time
from datetime import timedelta
from datetime import datetime
import threading

user = mqtt_connect.Client("C1")
delta = timedelta(seconds=10)
mensaje = ""
ahora = datetime.now()
contador = 0
salida = True

def on_subscribe(client, userdata,mid,granted_qos):
    print("subscribed: "+str(mid)+" "+str(granted_qos))


user.on_subscribe = on_subscribe


user.connect("broker.mqtt-dashboard.com", port=1883)
user.subscribe("conjunto1/residencia1/heartbeathub")

address = ['af.pinzon10@uniandes.edu.co']
sender = 'zl.castaneda10@uniandes.edu.co'

def listen_heartbeat():
    global salida, ahora,contador
    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(mensaje)

    while salida:
        while ahora + delta > datetime.now():


            time.sleep(1)

            if "alive" in mensaje:
                contador = 0
                ahora = datetime.now()


        contador += 1
        print(contador)
        if contador >= 3:
            print("chucu chucu chucu")
            send_msg("Hub fuera de linea","Alerta Hub fuera de linea")
            salida = False

        ahora = datetime.now()


hiloheart = threading.Thread(target=listen_heartbeat)
hiloheart.start()

def on_message(user, data, message):
    global mensaje
    print("correo enviado")
    mensaje =  str(message.payload)
    if "fuera" in str(message.payload):
        send_msg(message.payload.decode('utf-8'), message.topic)


def send_msg(mensaje, asunto):
    print('De:', sender)
    print('Para:', address)
    print('Asunto: ', asunto)
    print('Mensaje: ', mensaje)

    mime_message = MIMEText(mensaje, "plain")
    mime_message["From"] = sender
    mime_message["To"] = " ,".join(address)
    mime_message["Subject"] = asunto

    try:
        smtp = smtplib.SMTP('smtp.office365.com')
        smtp.starttls()
        smtp.login(sender, 'Alfa_252')
        smtp.send_message(mime_message)
        print('Correo enviado')
        smtp.quit()
    except:
        print('Error: el mensaje no pudo ser enviado.')


user.on_message = on_message


user.loop_start()
time.sleep(1000)
user.loop_stop()
