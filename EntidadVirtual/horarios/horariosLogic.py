import datetime
import paho.mqtt.client as paho
import threading
import time

from click._compat import _force_correct_text_reader


def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


"""def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

"""
client = paho.Client()
client.on_publish = on_publish
"""client.on_subscribe = on_subscribe
client.on_message = on_message"""
client.connect("broker.mqtt-dashboard.com", 1883)
"""client.subscribe("conjunto1/residencia1/alerta")
#client.loop_forever()"""
topic = "conjunto1/residencia1/cerradura"


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
            client.publish(topic, "3;" + str(self.index), qos=0)
            self.estado = False


candados = []
candado1 = Candado(10, 15, 1, True)
candado2 = Candado(13, 18, 2, True)
candados.append(candado1)
candados.append(candado2)


def agregar_candado(hora_inicio, hora_fin, index, estado):
    cand = Candado(hora_inicio, hora_fin, index, estado)
    candados.insert(index, cand)


def borrar_candado(index):
    candados.pop(index)


def borrar_todos():
    global candados
    candados = []


def actualizador():
    while True:
        time.sleep(60)
        for c in candados:
            time.sleep(10)
            c.actualizar_estado()

a = threading.Thread(target=actualizador())
a.start()

