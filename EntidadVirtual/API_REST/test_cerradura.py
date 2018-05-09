from flask import Flask, request, jsonify


import paho.mqtt.client as paho
app = Flask(__name__)
topico = "conjunto1/residencia1/cerradura"
client = paho.Client()
client.connect("broker.mqtt-dashboard.com", 1883)

#Insertar una cerradura
@app.route("/cerradura", methods=["POST"])
def insert_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    hora_inicio = request.json['hora_inicio']
    hora_fin = request.json['hora_fin']

    nuevo_candado = "0;"+password+";"+posicion;

    #hl.agregar_candado(hora_inicio, hora_fin, posicion)
    client.publish("horariocandado", hora_inicio+";"+hora_fin+";"+posicion)
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)


@app.route("/cerradura", methods=["PUT"])
def update_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    nuevo_candado = "1;"+password+";"+posicion;
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)


@app.route("/cerradura", methods=["DELETE"])
def delete_cerradura():
    posicion = request.json['posicion']
    nuevo_candado = "2;" + posicion
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)



@app.route("/cerradura_all", methods=["DELETE"])
def delete_all_cerraduras():
    mensaje = "3"
    client.publish(topico,mensaje)
    return jsonify(mensaje)


@app.route("/cerraduraHorario", methods = ["PUT"])
def change_state_cerradura():
    posicion = request.json['posicion']
    mensaje = "4;"+posicion

if __name__ == '__main__':
    app.run(debug=True)



