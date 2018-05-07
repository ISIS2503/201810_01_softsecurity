#!/usr/bin/env python3
from email.mime.text import MIMEText
import paho.mqtt.client as mqtt_connect
import smtplib
import time

user = mqtt_connect.Client("C1")

user.connect("157.253.227.89", port=8083)
user.subscribe("conjunto1/residencia1/alerta")

address = 'arquisoftprueba@gmail.com'
sender = 'tv.huertas10@uniandes.edu.co'
smtp.login(sender, 'vanessa98')


def on_message(user, data, message):
    send_msg(message.payload.decode('utf-8'), message.topic)
    print('Calidad del mensaje: ', str(message.qos))


def send_msg(mensaje, asunto):
    print('De:', sender)
    print('Para:', address)
    print('Asunto: ', asunto)
    print('Mensaje: ', mensaje)

    mime_message = MIMEText(mensaje, "plain")
    mime_message["From"] = sender
    mime_message["To"] = address
    mime_message["Subject"] = asunto

    try:
        smtp = smtplib.SMTP('smtp.office365.com')
        smtp.starttls()
        smtp.send_message(mime_message)
        print('Correo enviado')
        smtp.quit()
    except:
        print('Error: el mensaje no pudo ser enviado.')


user.on_message = on_message

user.loop_start()
time.sleep(1000)
user.loop_stop()
