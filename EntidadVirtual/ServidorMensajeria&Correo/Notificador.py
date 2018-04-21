#!/usr/bin/env python3
import paho.mqtt.client as mqtt_connect
import smtplib
import time

user = mqtt_connect.Client("C1")

user.connect("172.24.42.91", port=8083)
user.subscribe("conjunto1/inmueble1/alerta")

destinatarios = ['Juan Camilo Useche Rodríguez <jc.useche10@uniandes.edu.co>', 'Zulma Lorena Castañeda <zl.castaneda10@uniandes.edu.co>', 'Andrés Felipe Pinzón <af.pinzon10@uniandes.edu.co>']
sender = "Tatiana Vanessa Huertas Bolaños <tv.huertas10@uniandes.edu.co>"


def on_message(user, data, message):
    print('De:', sender)
    print('Para:', destinatarios)
    print('Asunto: ', message.topic)
    print('Mensaje: ', message.payload.decode('utf-8'))
	email = 'From: {}\n 
			To: {}\n
			MIME-Version: 1.0\n
			Content-type: text/html\n
			Subject: {}'.format(sender, destinatarios, message.topic, message.payload.decode('utf-8'))
	try:
		smtp = smtplib.SMTP('localhost')
		smtp.sendmail(sender, destinatarios, email)
		print('Correo enviado')
	except:
		print('Error: el mensaje no pudo ser enviado.
		Comprobar sendmail instalado')


user.on_message = on_message

user.loop_start()
time.sleep(1000)
user.loop_stop()
