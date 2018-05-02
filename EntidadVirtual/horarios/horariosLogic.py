import datetime
import paho.mqtt.client as paho


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
client.subscribe("conjunto1/residencia1/alerta")
client.loop_forever()
topic = "conjunto1/residencia1/cerradura"


class Candado(object):
    def _init_(self, hora_inicio, hora_fin, index):
        self.horaInicio = hora_inicio
        self.horaFin = hora_fin
        self.index = index

    def dar_hora_inicio(self):
        return self.horaInicio

    def dar_hora_fin(self):
        return self.horaFin

    def dar_index(self):
        return self.index

    def actualizar_estado(self):
        if datetime.time.minute >= self.horaFin >= datetime.time.minute:
            client.publish(topic, "4;"+self.index, qos=0)
        elif datetime.time.minute <= self.horaFin <= datetime.time.minute:
            client.publish(topic, "3;" + self.index, qos=0)


candados = []
candado = Candado(44,45,1)
candados.append(candado)
while True:
    print("estoy en el while")
    candado.actualizar_estado()
