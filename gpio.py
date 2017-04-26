import RPi.GPIO as GPIO
import time

class PiControl:

	button_pin = 5
	photo_pin = 6

	def InitButton(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.button_pin, GPIO.IN)
		print("Pin {0} is currently: {1}".format(self.button_pin,GPIO.input(self.button_pin)))
	
	def ButtonStatus(self):
		return GPIO.input(self.button_pin)

	def InitPhoto(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.photo_pin, GPIO.IN)
		print("Pin {0} is currently: {1}".format(self.photo_pin,GPIO.input(self.photo_pin)))

	def PhotoStatus(self):
		return GPIO.input(self.photo_pin)


