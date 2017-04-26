import time
import argparse
import sys, traceback
import threading
import smbus
import room
import pymodbus

from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.server.sync import ModbusTcpServer

global server
global ip

def ServerThread(e):
	global server
	# Configure the service logging
	#import logging
	#logging.basicConfig()
	#log = logging.getLogger()
	#log.setLevel(logging.DEBUG)

	# Initialize your data store
	store = ModbusSlaveContext(
		di = ModbusSequentialDataBlock(0, [17]*100),
		co = ModbusSequentialDataBlock(0, [17]*100),
		hr = ModbusSequentialDataBlock(0, [17]*100),
		ir = ModbusSequentialDataBlock(0, [17]*100))
	context = ModbusServerContext(slaves=store, single=True)
	 
	# Initialize the server information
	identity = ModbusDeviceIdentification()
	identity.VendorName  = 'Pymodbus'
	identity.ProductCode = 'PM'
	identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
	identity.ProductName = 'Pymodbus Server'
	identity.ModelName   = 'Pymodbus Server'
	identity.MajorMinorRevision = '1.0'


	# Run the server 
	# StartTcpServer(context, identity=identity, address=(args.ip, 502))
	server = ModbusTcpServer(context, identity=identity, address=(ip, 502))
	print 'Server started'
	server.serve_forever(0.1)
	print 'Server stopped'

def RoomThread(update_interval, e):
	print 'Room thread starting'
	print 'Constructing room'

	client = ModbusTcpClient(ip)
	myRoom = room.MeetingRoom()	
	while True:
		if not e.isSet():
			roomInfo = myRoom.GetState()
			client.write_register(0, roomInfo["IsOccupied"])
			client.write_register(1, roomInfo["IsBooked"])
			client.write_register(2, roomInfo["BookerName"])
			client.write_register(12, roomInfo["PersonInRoom"])
			client.write_register(22, roomInfo["WebExInfo"])
			client.write_register(32, roomInfo["WebExPhone"])
			
			print 'Is Booked: ' + str(roomInfo['IsOccupied'])
		else:
			break
	client.close()
	print 'Room thread closing'


if __name__ == "__main__":
	global server
	global ip
	print "=== Modbus Device ==="
	parser = argparse.ArgumentParser(description='Modbus server')
	parser.add_argument('ip',  default='localhost', help='IP adress of modbus server')
	args = parser.parse_args()
	ip = args.ip
	
	
	e_exit = threading.Event()
	
	thServer = threading.Thread(name='ServerThread', target=ServerThread, args=(e_exit,))
	thRoom = threading.Thread(name='RoomThread', target=RoomThread, args=(10, e_exit,))
	thServer.start()
	thRoom.start()
	
	# Wait for keyboard interrupt
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "Stopping program"
	except Exception:
		traceback.print_exc(file=sys.stdout)
		
	
	
	# Set stop event for clients
	e_exit.set()

	# Shutdown server
	server.shutdown()

	# Wait until server shutdown
	while thServer.isAlive():
		time.sleep(0.01)
		
	# Stop the program
	print 'Done'
	sys.exit(0)
