from flask import Flask
import paho.mqtt.client as paho
from datetime import date as d

user = mqtt_connect.Client("C1")

user.connect('localhost', port=8083)
user.subscribe("conjunto1/residencia1/alerta")

def on_message(user, data, message):
    alarmas = mongo.db.alarmas
    data = '{"fecha":"' + d.day + '/' + d.month + '/' + d.year + ', "cerradura":1 , "immueble": 1, "conjunto": 1, "tipo": '
    if "P2" in message:
        data = data + '"Acceso no permitido" }'
        alarmas.insert(data)
    if "S1" in message:
        data = data + '"Intento de apertura sospechoso" }'
        alarmas.insert(data)
    if "M1" in message:
        data = data + '"Movimiento detectado" }'
        alarmas.insert(data)


user.on_message = on_message
user.loop_start()