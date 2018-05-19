import datetime
import paho.mqtt.client as paho
import threading
import time
from multiprocessing import Pipe

posicion = 0
hora_inicio = 0
hora_fin = 0

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = paho.Client()
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


candados = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
def agregar_candado(hora_inicio, hora_fin, pindex):
    global candados
    index=int(pindex)
    cand = Candado(hora_inicio, hora_fin, index, False)
    candados[index]=cand
    print("candado agregado")
    print(len(candados))


def borrar_candado(index):
    global candados
    candados.pop(index)


def borrar_todos():
    global candados
    candados = []


def actualizador():
    global candados
    while True:
        global candados
        print("aacr")
        time.sleep(10)
        print(len(candados))
        for c in candados:
            if not c == "0":
                # c.actualizar_estado()
                print(c.dar_index)
                print("se actualizo")


