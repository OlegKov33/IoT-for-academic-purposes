import json
import time

from Adafruit_IO import Client, Data  # pip3 install adafruit-io


class Adafruit():
    # This is where we get feeds from and this is what we use to publish
    aio = Client('AdafruitIO_Username', 'AdafruitIO_Active_Key')

#when you get adafruit data, this is how it looks:
#all instances of data if you want to get value you do: data[3]
#0 - created_epoh
#1 - created_at
#2 - updated_at
#3 - value
#4 - completed_at
#5 - feed_id
#6 - expiration
#7 - pisition
#8 - id
#9 - lat
#10 - lon
#11 - ele

##NOTES
# json.dumps() <--gets data
# json.loads() <--turns data usable
# is used when looking for specific value

#json.loads() <--loads data 
#json.dumps() <--turns data into suitable format so adafruit has (") instead of (')
# is unsed when uploading


    def __init__(self,name):
        self._name = name

        
    def upload(self,what,
                where,removed):
        
        self.add(what,where)                #Adds (what)-> data, to (where)-> feed
        data = self.aio.delete(where, removed)
        time.sleep(2)

        
    def getData(self,where):
        return self.aio.data(where)         #Gets data (where)->feed
            
        
    def create(self):
        sType = ""
        sGpio = 0
        sId = 0
        sAffects = "0"
        
        while sType != "heat" and sType != "motion" and sType != "led" and sType != "button":
            sType = str(input("Enter the device type from the list (heat, motion, led, button): ")).lower() #sets sensor type to (heat,motion,led or button)
            
        while sGpio>=28 or sGpio <=1:
            sGpio = int(input("Enter the device gpio pin in range(2-27): "))                                #sets gpio from 2 to 27
            
        while sId <1:
            sId = int(input("Enter device ID, 1 or higher: "))                                              #assignes id
            
        if sType == "button":
            sAffects = int(input("Which gpio does it affect in range(2-27): "))                             #if you have a button you need to select which gpio it will turn off
        else:
            sAffects = int(sAffects)                                                                        #otherwise sets it to 0
            
        sGpio  =str(sGpio)
        temp = {"type":sType, "state":"0","gpio":sGpio,"affects":sAffects,"condition":"0","id":sId}         #builds data
        temp2 = json.dumps(temp)                                                                            #makes data usable by adafruit
        tempType = sType+"s"                                                                                #finds feed where the data will go
        self.add(temp2,tempType)                                                                            #calls a function which adds data to adafruit


    def add(self,collection,
            place):
        
        data = Data(value=collection)
        self.aio.create_data(place, data)           #adds data to adafruit (place)->feed and (data)->looks like temp above
        print("I add things to adafruit")           #indicates that adafruit has been updated
        
        
    def preset(self):
        self.clearAll()                                                                                 #a function that removes everything from feeds
        where = ["heats","motions","buttons","leds"]
        self.add('{"type":"heat","state":"1","gpio":"14","affects":0,"condition":"0","id":1}',where[0]) #adds data to feed(heats) because there is no way to turn on heat sensor, it has been set to be on permanently
        self.add('{"type":"motion","state":"0","gpio":"4","affects":0,"condition":"0","id":2}',where[1])#adds data to feed(motions)
        time.sleep(2)
        self.add('{"type":"button","state":"0","gpio":"4","affects":4,"condition":"0","id":3}',where[2])#adds data to feed(buttons)
        self.add('{"type":"button","state":"0","gpio":"5","affects":3,"condition":"0","id":4}',where[2])
        self.add('{"type":"button","state":"0","gpio":"6","affects":14,"condition":"0","id":5}',where[2])
        time.sleep(2)
        self.add('{"type":"led","state":"0","gpio":"7","affects":0,"condition":"0","id":6}',where[3])   #adds data to feed(leds)
        self.add('{"type":"led","state":"0","gpio":"8","affects":0,"condition":"0","id":7}',where[3])
        self.add('{"type":"led","state":"0","gpio":"9","affects":0,"condition":"0","id":8}',where[3])
        #print("this loads preset: 1 motion, 1 heat, 3 button, 3 leds")
    


    def clearAll(self):
        where = ["heats","motions",
                "buttons","leds"]
        what = "temp"                               #adds value temp to all feeds in (where) as if you try and delete data that doesn't exist you will get an error
        self.add(what,where[0])
        self.add(what,where[1])
        self.add(what,where[2])
        self.add(what,where[3])
        
        h1 = self.aio.data('heats')                 #gets data from feed(heats)
        m1 = self.aio.data('motions')               #gets data from feed(motions)
        b1 = self.aio.data('buttons')               #gets data from feed(buttons)
        l1 = self.aio.data('leds')                  #gets data from feed(leds)
        
                                                    #deletes data in all feeds
        for rH in h1:
            h1 = self.aio.delete('heats', rH[8])
            print("removed heat sensor")
        time.sleep(2)
        
        for rM in m1:
            m1 = self.aio.delete('motions', rM[8])
            print("removed motion sensor")
        time.sleep(2)
        
        for rB in b1:
            b1 = self.aio.delete('buttons', rB[8])
            print("removed button")
        time.sleep(2)
        
        for rL in l1:
            l1 = self.aio.delete('leds', rL[8])
            print("removed led")
            
    #heats - stores all devices which are "heat" sensors
    #motions - stores all devices with are "motion" sensors
    #buttons - stores all devices which are "buttons"
    #leds - stores all dedivces which are "leds"

            
    def test(self):
        print("I work")                             #here it checks if you are connected to file or not

