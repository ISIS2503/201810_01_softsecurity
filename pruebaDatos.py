#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time

client = mqtt.Client("C1")


client.connect("172.24.42.91", port = 8083 ) 
client.suscribe("alert/wiring/+)


def on_message(client, data, message)
	print( "message received:" + str(message.payload.decode("utf-8))
	print( "message topic: " + message.topic)
	print ( "message qos : " + str(message.qos))
	
	
client.on_message = on_message
	
client.loop_start()
time.sleep(1000)
client.loop_stop()