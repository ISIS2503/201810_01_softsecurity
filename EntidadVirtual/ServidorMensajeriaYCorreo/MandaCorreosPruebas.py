#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt_connect

user = mqtt_connect.Client("C2")

user.connect('localhost', port=8083)
error = 0
alarmas = 300000
tiempoinicial = time.time()

for i in range(0, alarmas):
    user.publish("conjunto1/residencia1/alerta", payload='Alerta, Intruso!!!')

tiempofinal = time.time() - tiempoinicial
print('Tiempo de envío en segundos:', tiempofinal)
print('Porcentaje de error: ' + str(error) + '%')


