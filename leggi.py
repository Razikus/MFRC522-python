#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the RC522 data read example"
print "Press Ctrl-C to stop."

uid_buffer = 0
keys = [ [0xD3,0xF7,0xD3,0xF7,0xD3,0xF7] ] #, [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5]], [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], [0x00,0x00,0x00,0x00,0x00,0x$

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    #ToDo: should be 0-63 eccetto le quarte
    for sector in range(4,6):
        #ToDo: check this, add break on fail
        #for key in keys:
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK: #and uid != uid_buffer:

            # Store UID in buffer
            uid_buffer = uid

            # Print UID
            #print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        
            # This is the default key for authentication
            key = [0xD3,0xF7,0xD3,0xF7,0xD3,0xF7] 
            
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                #ToDo: store content in buffer
                x = MIFAREReader.MFRC522_Read(8)
                print(x)
                MIFAREReader.MFRC522_StopCrypto1()
                #MIFAREReader.MFRC522_Init()
            else:
                print "Authentication error"
                #ToDo: rimuovere in produzione, handle errore
                continue_reading = False

