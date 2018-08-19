# Forked by Simon Monk at https://github.com/simonmonk/

import MFRC522
import RPi.GPIO as GPIO
	
class SimpleMFRC522:

	READER = None;
	
	KEY = [0xD3,0xF7,0xD3,0xF7,0xD3,0xF7]
	KEYB= [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5]
	KEYS= [ [0xD3,0xF7,0xD3,0xF7,0xD3,0xF7], [0xA0,0xA1,0xA2,0xA3,0xA4,0xA5] ]
	BLOCK_ADDRS = [4, 5, 6, 8, 9, 10] #124
	
	def __init__(self):
		self.READER = MFRC522.MFRC522()
	
	def read(self,blocco,chiave):
		#auth_place = int(blocco/4)*4
		settore = blocco * 4
		id, text = self.read_no_block(settore,self.KEYS[chiave])
		#while not id:
		#id, text = self.read_no_block(settore,self.KEY)
		return id, text

	def get_id(self):
		id = self.get_no_id()			
		while not id:
			id = self.get_no_id()
		return id
	
	def read_no_block(self, blocco, chiave):
		(status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
		if status != self.READER.MI_OK:
				return None, None
		(status, uid) = self.READER.MFRC522_Anticoll()
		if status != self.READER.MI_OK:
				return None, None
		id = self.uid_to_num(uid)

		self.READER.MFRC522_SelectTag(uid)

		data = []
		text_read = ''

		if status == self.READER.MI_OK:
			status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, blocco, chiave, uid)
			if status == self.READER.MI_OK:
				for settore in range(blocco,blocco+4):
					print("Auth %s - Settore %s" %(blocco,settore))
					block = self.READER.MFRC522_Read(settore)
					if block:
						data += block
			else:
				print("ERRORACCIOOOOOOO")
				self.READER.MFRC522_StopCrypto1()

		if data:
			text_read = ''.join(chr(i) for i in data)
		self.READER.MFRC522_StopCrypto1()

		return id, text_read
		
	def get_no_id(self):
		(status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
		if status != self.READER.MI_OK:
				return None, None
		(status, uid) = self.READER.MFRC522_Anticoll()
		if status != self.READER.MI_OK:
				return None, None
		id = self.uid_to_num(uid)
		return uid, id
		
	def write(self, text):
			id, text_in = self.write_no_block(text)				
			while not id:
					id, text_in = self.write_no_block(text)	
			return id, text_in


	def write_no_block(self, text):
			(status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
			if status != self.READER.MI_OK:
					return None, None
			(status, uid) = self.READER.MFRC522_Anticoll()
			if status != self.READER.MI_OK:
					return None, None
			id = self.uid_to_num(uid)
			self.READER.MFRC522_SelectTag(uid)
			status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 4, self.KEY, uid)
			self.READER.MFRC522_Read(4)
			if status == self.READER.MI_OK:
					data = bytearray()
					data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
					i = 0
					for block_num in self.BLOCK_ADDRS:
						self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
						i += 1
			self.READER.MFRC522_StopCrypto1()
			return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
			
	def uid_to_num(self, uid):
			n = 0
			for i in range(0, 5):
					n = n * 256 + uid[i]
			return n
