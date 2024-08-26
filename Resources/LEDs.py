import json
from Resources.Adafruit import Adafruit # pip3 install adafruit-io
import time
from sense_hat import SenseHat # pip install sense-hat
class LEDs:
	ada = Adafruit("name")
	sense = SenseHat()
	
	def __init__(self,name):
		self._name = name
		
		
	def getData(self,where):
		return self.ada.getData(where)
	
	
	def process(self):
		total = 0							#number of devices seen
		counter = 0							# number of devices that are not disabled and turned on
		searchHere = ["heats","motions"]
		
		for sensor in range(len(searchHere)):				#loops through feeds heats and motions
			tempSensor = self.getData(searchHere[sensor])		#tempSensor is a variable with data from feed
			for temp in range(len(tempSensor)):			#for each instance of data in tempSensor loop
				tempJSON = json.loads(tempSensor[temp][3])	#convert to JSON,[3] is value which is (type,state,gpio,affects...)
				tempJSON["condition"] = int(tempJSON["condition"])#converts condition value from string to integer
				tempJSON["state"] = int(tempJSON["state"])	#converts state value from string to integer
				
				if tempJSON["condition"] == 1:			#if the sensor is disabled, add to total but not to counter
					total +=1
				else:						#otherwise check if the sensor is on or off
					if tempJSON["state"] == 1:		#if the sensor is on increase total and counter
						total +=1
						counter +=1
					else:					#otherwise increase total
						total += 1
		time.sleep(1)
		if total == counter:						#if all devices are on, call green function
			self.green()
			
			
		elif counter>0:							#if at least 1 device is on call yellow function
			self.yellow()
			
		else:								#if neither of above is true call red function
			self.red()
			
			
	def red(self):
		r = 255
		g = 0
		b = 0
		self.sense.clear((r, g, b))

		
	def yellow(self):
		r = 255
		g = 255
		b = 0
		self.sense.clear((r, g, b))
		

	def green(self):
		r = 0
		g = 255
		b = 0
		self.sense.clear((r, g, b))
		
