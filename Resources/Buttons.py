import json

from gpiozero import Button  # sudo apt install python3-gpiozero
from Resources.Adafruit import Adafruit  # pip3 install adafruit-io


class Buttons():
	ada = Adafruit("name")
	
	
	def __init__(self,name):
		self._name = name
		
		
	def process(self):
		where = "buttons"
		buttons = self.ada.getData(where) 		#gets data from feed named "buttons"
		
		for buttonX in buttons:				#loops throught each button
			buttonXJSON = json.loads(buttonX[3])	#convert to json
			value = self.value(buttonXJSON["gpio"]) #checks if the button is on or off
		
			if value == 1:				# check if its on run on() function
				self.on(buttonXJSON, buttonX)
			else:
				self.off(buttonXJSON, buttonX) 	# check if its on run off() function
	
	
def on(self, buttonXJSON
       	,buttonX):
	where = "buttons"
	# check if sensor is on online
	if buttonXJSON["state"] !="1":			#if the button is 0(off) uploads to buttons feed new button "state" value
		buttonXJSON["state"] = "1"
		self.upload(buttonXJSON, buttonX,where)
	self.process2N(buttonXJSON)			#continue process


def off(self,buttonXJSON, 
	buttonX):
	where = "buttons"
	# check if sensor is off online
	if buttonXJSON["state"] !="0":			#if the button is 1(on) uploads to buttons feed new button "state" value
		buttonXJSON["state"] = "0"
		self.upload(buttonXJSON, buttonX,where)
	self.process2F(buttonXJSON)			#continue process	
		
		
def process2N(self, buttonXJSON):
	feeds = ["motions","heats"]
	length = len(feeds)
	for temp in range(length):				#loops heats and motions feeds
		for sensorX in self.ada.getData(feeds[temp]):#for each instance of data
			tempSensor = sensorX[3]		#make tempSensor equal to its value (type,state,gpio,affects...)
			tempJSON  = json.loads(tempSensor)	#converts to json
			if str(tempJSON["gpio"])== str(buttonXJSON["affects"]):	#checks if button affects the sensors gpio 
				if tempJSON["condition"] != "1":			#checks if the sensor is off(0) online
					tempJSON["condition"] = "1"			#if its off, sets it on and upload
					self.upload(tempJSON, sensorX,feeds[temp])
		    
		
def process2F(self, buttonXJSON):
	feeds = ["motions","heats"]
	length = len(feeds)
	for temp in range(length):				#loops heats and motion feeds
		for sensorX in self.ada.getData(feeds[temp]):#for each instance of data
			tempSensor = sensorX[3]		#make tempSensor equal to its value (type,state,gpio,affects...)
			tempJSON  = json.loads(tempSensor)	#converts to json
			if str(tempJSON["gpio"])== str(buttonXJSON["affects"]):	#checks if button affects the sensors gpio
				if tempJSON["condition"] != "0":			#checks if the sensor is on(1) online
					tempJSON["condition"] = "0"			#if its on, sets it off and upload
					self.upload(tempJSON, sensorX,feeds[temp])
		
		
def upload(self, buttonXJSON, buttonX,where):
	tempID = buttonX[8]				#finds feed ID that is unique to every feed
	buttonXJSON = json.dumps(buttonXJSON)		#converts data into suitable format for adafruit so that data looks like (") and not (')
	self.ada.upload(buttonXJSON,where,tempID)	#uploads
	  

def value(self, gpio):
	zeroButtonX = Button(gpio)	#creates a button at a specific gpio
	return zeroButtonX.value	#checks that gpio for input and returns its value (1/0)
          
