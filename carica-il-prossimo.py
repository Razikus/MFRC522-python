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

def scrivi(cosa):
	reader = SimpleMFRC522.SimpleMFRC522()
	try:
		reader.write(cosa)
		print("Written")
	finally:
		GPIO.cleanup()
	return

scrivi(token)
