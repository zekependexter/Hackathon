from gpio import PiControl
from room import MeetingRoom
import time

if __name__ == '__main__':

	pi = PiControl()
	room = MeetingRoom()
	
	print("Initializing GPIO pins...")	
	pi.InitButton()
	pi.InitPhoto()
	print("Initialization done!")
	print("We are in: {0}".format(room.Name))

	while(1):
		if(pi.ButtonStatus() == 0):
			print("Button Pressed")
			while(pi.ButtonStatus() == 0):
				time.sleep(.1)	
			print("Button Depressed")
			room.SetOccupiedState()

			roomstate = room.GetState
			print("Room state is: {0}".format(roomstate))

		if(pi.PhotoStatus() == 1):
			print("Photo Triggered")
			while(pi.PhotoStatus() == 1):
				time.sleep(.1)	
			print("Photo Un-Triggered")
			room.SetOccupiedState()

		
