from flask import Flask
import time
import paho.mqtt.client as paho
app = Flask(__name__)
broker="broker.hivemq.com"


#Insertar una cerradura
@app.route("/cerradura", methods=["POST"])
def insert_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    hora_inicio = request.json['hora_inicio']
    hora_fin = request.json['hora_fin']

    nuevo_candado = "0;"+password+";"+posicion;
    #Escribir y publicar mensaje


@app.route("/cerradura", methods=["UPDATE"])
def update_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    nuevo_candado = "1;"+password+";"+posicion;


@app.route("/cerradura", methods=["DELETE"])
def delete_cerradura():
    posicion = request.json['posicion']
    nuevo_candado = "2;" + posicion;

@app.route("/cerradura_all", methods=["DELETE"])
def delete_all_cerraduras():
    mensaje = "3"


@app.route("/cerradura", methods = ["PUT"])
def change_state_cerradura():
    posicion = request.json['posicion']
    mensaje = "4;"posicion;

if __name__ == '__main__':
    app.run(debug=True)
