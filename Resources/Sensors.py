import json

from gpiozero import MotionSensor  # sudo apt install python3-gpiozero
from Resources.Adafruit import Adafruit  # pip3 install adafruit-io


class Sensors():
    ada = Adafruit("name")
    
    
    def __init__(self,name):
        self._name = name
        
        
    def process(self):
      where = "motions"
      sensors = self.ada.getData(where)                         #get data from feed called "motions"
      zeroSensorX = MotionSensor(0)
      for sensorX in sensors:                                   #for each sensor in motions feed 
        sensorXJSON = json.loads(sensorX[3])                    #convert to JSON
        value = self.value(sensorXJSON["gpio"])                 #call function which returns the value of current sensor at specific gpio port
        
        if value == 1:                                          #if the sensor is on(1) call on() function
          self.on(sensorXJSON, sensorX)
        else:                                                   #otherwise call off() function
          self.off(sensorXJSON, sensorX)
    
    
    def on(self, sensorXJSON, sensorX):
      if sensorXJSON["state"] !="1":                            #if the sensor state is not on(1)
        sensorXJSON["state"] = "1"                              #make it 1
        self.upload(sensorXJSON, sensorX)                       #upload online to adafruit
        
        
    def off(self,sensorXJSON, sensorX):
        if sensorXJSON["state"] !="0":                          #if the sensor state in not off(0)
          sensorXJSON["state"] = "0"                            #make it 0
          self.upload(sensorXJSON, sensorX)                     #upload online to adafruit
        
        
    def upload(self, sensorXJSON, sensorX):
      tempID = sensorX[8]                                       #feed id that you will be deleting
      where = "motions"                                         #feed name where you are going to create data in
      sensorXJSON = json.dumps(sensorXJSON)                     #convert to suitable format for adafruit so it stores data in (") and not (')
      self.ada.upload(sensorXJSON,where,tempID)                 #call a function which uploads to adafruit
      

    def value(self, gpio):
      zeroSensorX = MotionSensor(gpio)                          #makes a motion sensor at specified gpio
      return zeroSensorX.value                                  #checks if that gpio is on or off (1/0)
          
