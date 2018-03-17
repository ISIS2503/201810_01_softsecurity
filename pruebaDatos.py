#!/usr/bin/env python3
import paho.mqtt.client as mqttConnect
import time

user = mqttConnect.Client("C1")


user.connect("172.24.42.91", port = 8083 ) 
user.subscribe("alert/#")


def on_message(user, data, message):
	print( "message received: " + str(message.payload.decode("utf-8")))
	print( "message topic: " + message.topic)
	print( "message qos : " + str(message.qos))
	
	
user.on_message = on_message
	
user.loop_start()
time.sleep(1000)
user.loop_stop()