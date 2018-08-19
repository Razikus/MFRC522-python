#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import threading
from flask import Flask
import time
import random

app = Flask(__name__)
token = "qk@77Ek5qnPvUtB_jgHu]af9L8ex-UV7@?P#+wune{LG6Td!!c3CffMfCrKvWYW9"
nope = "000xxx000xxx"
global value1
value1 = 0

def leggi():
	b = 3
	g = 5
	r = 7
	led = [r,g,b]
	id_buffer = 0
	last_id = 0

	reader = SimpleMFRC522.SimpleMFRC522()

	while(True==True):
		try:
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(b,GPIO.OUT)
			GPIO.setup(g,GPIO.OUT)
			GPIO.setup(r,GPIO.OUT)
			GPIO.output(b, 1)
			time.sleep(0.5)
			GPIO.output(b, 0)
			time.sleep(0.2)
			GPIO.output(b, 1)

			id, text = reader.read()
			if(id) and (text):
				#print(id)
				print(text)
				credito = 0

				if(id_buffer!=id):
					id_buffer=id
					last_id=time.time()
					flicker10s=False
					last_credito=0

					if(text):
						if(text in token) or (intern(text) is intern(token)) or (token in text) or (text==token):
							credito = 1

					if(credito>0):
						print("SI")
						GPIO.output(g, 1)
						time.sleep(0.5)
						GPIO.output(g, 0)
						time.sleep(0.2)
						GPIO.output(g, 1)
						global value1
						value1 += 1
						scrivi(nope)
					else:
						print("NO!")
						GPIO.output(r, 1)
						time.sleep(0.5)
						GPIO.output(r, 0)
						time.sleep(0.2)
						GPIO.output(r, 1)
				elif(time.time()>last_id+10) and (flicker10s==False):
					print("BEN TEEEEN")
					flicker10s=True
					if(last_credito<0):
						print("NO!")
						GPIO.output(r, 1)
						time.sleep(0.5)
						GPIO.output(r, 0)
						time.sleep(0.2)
						GPIO.output(r, 1)
					elif(last_credito>0):
						print("SI")
						GPIO.output(g, 1)
						time.sleep(0.5)
						GPIO.output(g, 0)
						time.sleep(0.2)
						GPIO.output(g, 1)
						global value1
						value1 += 1
						scrivi(nope)
				else:
					print ("STESSA, non fare nulla")

		finally:
			GPIO.cleanup()
	return

def scrivi(cosa):
	reader = SimpleMFRC522.SimpleMFRC522()
	try:
		reader.write(cosa)
		print("Written")
	finally:
		GPIO.cleanup()
	return

@app.route('/')
def home():
    return "WS OK!"

@app.route('/bar1')
def bar1():
	global value1
	return str(value1)

if __name__ == '__main__':
    threading.Thread(target=leggi).start()
    app.run(host='0.0.0.0', port=4000, threaded=True)

#leggi()
#scrivi(token)
