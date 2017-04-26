import RPi.GPIO as GPIO
import time

class PiControl:

	button_pin = 5

	def InitButton(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.button_pin, GPIO.IN)
		print("Pin {0} is currently: {1}".format(self.button_pin,GPIO.input(self.button_pin)))
	

class Ledarray:

	LED_Array = [2,3,4,5,6,7,8,9,10,11]
	GPIO.setmode(GPIO.BCM)

	for led in LED_Array:
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led, GPIO.LOW)
	
	def FlickerLightsUp(self):
		for led in self.LED_Array:
			GPIO.output(led, GPIO.HIGH)
			time.sleep(.01)
#			print("Lighting LED {0}".format(led))
			GPIO.output(led, GPIO.LOW)


	def FlickerLightsDown(self):
		for led in self.LED_Array:
			led_num = 13 - led
			GPIO.output(led_num, GPIO.HIGH)
#			print("Lighting LED {0}".format(led_num))
			time.sleep(.01)
			GPIO.output(led_num, GPIO.LOW)
