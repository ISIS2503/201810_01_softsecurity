#!/usr/bin/env python3
from email.mime.text import MIMEText
import paho.mqtt.client as mqtt_connect
import smtplib
import time

user = mqtt_connect.Client("C1")

user.connect("172.24.42.91", port=8083)
user.subscribe("conjunto1/inmueble1/alerta")

adress = ['Ju<jc.useche10@uniandes.edu.co>', 'Zul<zl.castaneda10@uniandes.edu.co>', 'An<af.pinzon10@uniandes.edu.co>']
sender = "Tatiana Vanessa Huertas Bolaños <tv.huertas10@uniandes.edu.co>"


def on_message(user, data, message):
    print('De:', sender)
    print('Para:', adress)
    print('Asunto: ', message.topic)
    print('Mensaje: ', message.payload.decode('utf-8'))

    mime_message = MIMEText(message.payload.decode('utf-8'), "plain")
    mime_message["From"] = sender
    mime_message["To"] = adress
    mime_message["Subject"] = message.topic

    try:
        smtp = smtplib.SMTP('localhost')
        smtp.login(sender, "Password")
        smtp.sendmail(sender, adress, mime_message.as_string())
        print('Correo enviado')
    except:
        print('Error: el mensaje no pudo ser enviado. Comprobar sendmail instalado')
        smtp.quit()


user.on_message = on_message

user.loop_start()
time.sleep(1000)
user.loop_stop()
