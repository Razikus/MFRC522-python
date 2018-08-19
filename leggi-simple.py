#!/usr/bin/env python
# Looking for:
# 1, 8, 84, 2, 101, 110, 112, 114, 111, 118, 97, 254, 0, 0, 0, 0 -> OK
# ID -> 345012929496 (in int)


import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
		uid = reader.id()
		print(uid)
        id, text = reader.read()
        print(id)
        print(text)
finally:
        GPIO.cleanup()