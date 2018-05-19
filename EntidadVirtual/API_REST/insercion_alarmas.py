from flask import Flask
import paho.mqtt.client as paho

user = mqtt_connect.Client("C1")

user.connect('localhost', port=8083)
user.subscribe("conjunto1/residencia1/alerta")

def on_message(user, data, message):
    alarmas = mongo.db.alarmas
    if 


user.on_message = on_message
user.loop_start()