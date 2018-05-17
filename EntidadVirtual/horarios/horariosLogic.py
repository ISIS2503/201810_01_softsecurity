import datetime
import paho.mqtt.client as paho
import threading
import time

posicion = 0
hora_inicio = 0
hora_fin = 0

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_publish = on_publish
topic = "conjunto1/residencia1/cerradura"
client.connect("broker.mqtt-dashboard.com", 1883)

class Candado(object):
    def __init__(self, hora_inicio, hora_fin, index, estado):
        if hora_fin < hora_inicio:
            hora_fin += 60
        self.horaInicio = hora_inicio
        self.horaFin = hora_fin
        self.index = index
        self.estado = estado

    def dar_hora_inicio(self):
        return self.horaInicio

    def dar_hora_fin(self):
        return self.horaFin

    def dar_index(self):
        return self.index

    def dar_estado(self):
        return self.estado

    def actualizar_estado(self):
        hor = datetime.datetime.now().minute
        if hor < self.horaInicio:
            hor += 60
        if self.horaInicio <= hor <= self.horaFin and not self.estado:
            client.publish(topic, "4;"+ str(self.index), qos=0)
            self.estado = True
        elif self.estado:
            client.publish(topic, "2;" + str(self.index), qos=0)
            self.estado = False


candados = []


def agregar_candado(hora_inicio, hora_fin, index):
    cand = Candado(hora_inicio, hora_fin, index, False)
    candados.insert(index, cand)
    print("candado agregado")
c = agregar_candado(50,53,5)
c2 = agregar_candado(13,17,2)


def borrar_candado(index):
    candados.pop(index)


def borrar_todos():
    global candados
    candados = []


def actualizador():
    print("aacr")
    while True:
        for c in candados:
            time.sleep(10)
            c.actualizar_estado()

def on_message(client, userdata, msg):
    global hora_inicio,hora_fin,posicion
    x=str(msg.payload)
    x=x[2:-1]
    print(x)
    hora_inicio, hora_fin, posicion = x.split(";")
    agregar_candado(int(hora_inicio),int(hora_fin),int(posicion))
client.on_message = on_message
a = threading.Thread(target=actualizador())
a.start()

client.subscribe("horariocandado")
client.loop_forever()




print("end")

