from flask import Flask
from flask_pymongo import PyMongo
import paho.mqtt.client as paho
from datetime import date as d
import time
import json


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)

user = paho.Client()



def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_message(user, data, message):
    print(str(message.payload))
    m = str(message.payload)
    with app.app_context():
        alarmas = mongo.db.alarmas
        data = '{ "fecha":"' + d.today().day.__str__() + '/' + d.today().month.__str__() + '/' + d.today().year.__str__() + '", "cerradura":1 , "immueble": 1, "conjunto": 1, "tipo": '
        if "P2" in m:
            data = data + '"Acceso no permitido" '
            alarmas.insert(data)
        if "S1" in m:
            data = data + '"Intento de apertura sospechoso" '
            alarmas.insert(data)
        if "M1" in m:
            data = data + '"Movimiento detectado" }'
            alarmas.insert(json.loads(data))
        print(data)

def on_subscribe(client, userdata,mid,granted_qos):
    print("subscribed: "+str(mid)+" "+str(granted_qos))

user.on_connect = on_connect
user.on_subscribe = on_subscribe

user.on_message = on_message
user.connect("broker.mqtt-dashboard.com", port=1883)
print("suscribe 1")
user.subscribe("conjunto1/residencia1/alerta")
print("suscribe 2")
user.loop_forever()

if __name__ == "__main__":
    app.run()