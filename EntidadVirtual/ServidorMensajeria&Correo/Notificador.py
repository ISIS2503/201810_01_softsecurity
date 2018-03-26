#!/usr/bin/env python3
import paho.mqtt.client as mqtt_connect
import time

user = mqtt_connect.Client("C1")

user.connect("172.24.42.91", port=8083)
user.subscribe("conjunto1/inmueble1/alerta")

destinatarios = ['jc.useche10@uniadnes.edu.co', 'zl.castaneda10@uniandes.edu.co', 'af.pinzon10@uniandes.edu.co']
sender = 'tv.huertas10@uniandes.edu.co'


def on_message(user, data, message):
    print('De:', sender)
    print('Para:', destinatarios)
    print('Asunto: ', message.topic)
    print('Mensaje: ', message.payload.decode('utf-8'))


user.on_message = on_message

user.loop_start()
time.sleep(1000)
user.loop_stop()
