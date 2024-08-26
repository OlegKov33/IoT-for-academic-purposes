[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Y_QRUVPr)

# CM2110-IOT-coursework
> [!Note]
> This project was done as a part of a university module in the 2022-23 academic year. It will be posted as archive material to showcase my skills.
```
 Team name: [Titan]
```

# User Profile:
Originally this project was created without the purpose of solving some real-world issue but rather to simply help with boredom, which it remains. This project is useful for people who don't know what to do, in this project they will see how different sensors are being used as input which can be changed with buttons and displayed on the senseHAT matrix. In this project, you -- the stakeholder -- will learn: how to get input from sensors, how the buttons are used to alter the input, how it is displayed and how Adafruit IO is used to store data in its feeds. Another stakeholder that might benefit from this project is a teacher, as it can be used as an example of open-source code that can be analysed, used and reflected on, to determine its strengths and weaknesses by teacher or their students.

# System Design:
 In this section, you will find out how things work behind the scenes. In the image below you can see that star topology is being used where adafruit IO is the centre of.
[Figure 1]
![Figure 1](/Media/FINAL%20IoT%20image%20(1).png/)


What's IoT? IoT means Internet of Things and it means that a device or a group of devices - that have different shapes, forms and abilities - have the ability to be connected to the Internet and exchange data with other devices. SenseHAT is a great example of an I/O(input, output) device as it allows you to not only get data from its sensors but also display data using an LED matrix. SenseHAT has multiple sensors and actuators that can be used as input, for example: a temperature sensor that can be used if you are trying to see the temperature, the temperature can range from -40 up to 120 degrees Celsius and can be used in real-world case such as measuring room or fridge temperature, but it's a bad idea as there are devices that are made for a specific job and thus will give you more accurate and reliable output. Think of it as an infrared thermometer vs a thermometer for adults when you are measuring human temperature. LED matrix(8x8) is another device that can be found on senseHAT but this device outputs rather than inputs data, it does that by colouring a specific pixel - or a group of pixels - with RGB(red, green, blue) value from 0-255 (0,0,0 - Black) (255,255,255 - White). Since senseHAT can't work on its own it needs to connect to Raspberry Pi's general purpose input-output (GPIO) pins which there are forty of on model 3B+. Other than senseHAT we also used buttons and PIR sensors both of which are significantly cheaper options than senseHAT and they are single-purpose. The buttons have 4 pins and those are connected to each other and based on the button state (pressed or released) you can get various inputs for example: if you press the button and have wires connected diagonally to it (like we did) you will close the circuit and send a pulse which - with use of code - you can track to determine if it's 1 or 0. PIR has 3 pins and works by using heat-detecting sensors which check the surrounding area for heat change and when it is detected the output goes to high (1). In order for the above to work you need to use Raspberry Pi which is a low-cost computer - a side note: you can also use Arduino for buttons and pir but not for senseHAT - which is capable of getting input from USB(Universal Serial Bus) devices such being keyboards, mice, it can also connect things like ethernet, video and power cables and has the ability to connect to the network wirelessly. Raspberry Pi 3B+ has 40 GPIO pins from which there are: x26 GPIO, x8 ground, x2 5V power, x2 3.3V power and x2 EEPROM (ID_SE and ID_SD). We also need a gpiozero library in order to get input from buttons and PIR into Python which is a programming language which is OOP(object-oriented programming) and is an interpreter.


After we discussed the physical side, let's go into protocols that are used to transfer data from device to device. To do that we use adafruit IO which is an open-source cloud service which you can connect to using the Internet. In order to use it you need to use an API which uses MQTT(Message Queuing Telemetry Transport) protocol which uses brokers to publish/subscribe models of data to those devices which are connected to a specific topic using the Internet, MQTT is very light and doesn't encrypt its data which is why you might want to consider using SSL(Secure Sockets Layer) which is a technology used to establish and encrypting link between server and client. But let's get back to MQTT, MQTT has three levels of sending data: level 0 is only sending data without ensuring if the data was received (UDP), level 1 sends data at least once and asks if they are received and may cause duplication, and last is level 2 which only sends the message once and ensure that it has or hasn't been received to then send it again (TCP). Adafruit IO is used as a broker where you use [feeds](/Media/imageX.png) as your topics in which you store data in the form of "time-series databases" which have a specific date/time for specific records and that will be lost after 30 days. In order to access specific topics ([feeds](/Media/imageX.png)) you need to have a few things: a username and a key as well as a feed key, feeds can either be public or private (private: only you can see it and edit it)(public: everyone can see it but can't edit it).


Let's look at how it works with actuators and protocols, we used four Raspberry Pis each with its own purpose: Creation RPI is a node that is responsible for creating and posting data to Adafruit as well as deleting it, in order to create data you need to use adafruit_IO API(Application Programming Interface) library which you can download in Adafruit.py file, we used it with one (username, key) and varied [feed](/Media/imageX.png) keys(feed key is usually feed name but in lower case) after we established connection to broker(feed) we can post data using [create_data](https://adafruit-io-python-client.readthedocs.io/en/latest/data.html#data-creation)("feed key", data ) method, more on which can be found here CLICKME the way we get data is by using data("feed key") method, which uses a specific feed in order to subscribe to it, lastly we used to delete("feed key", ([ID](/Media/Screenshot%202023-04-20%20105118.png))) method to find a specific value in feed and remove it. After we added(temp), viewed, deleted and created data. The data that we used has the following format: {"type":"led","state":"0","gpio":"9","affects":0,"condition":"0","id":8}
- type("str"): a type of device we got and adding "s" to the end tells us in which [feed](/Media/imageX.png) to place it
- state("str"): whether or not the device is on or off (1/0)
- gpio("str"): on which GPIO pin you can find it in one of the 26 available.
- affects(int): is what is GPIO will be exclusive to buttons as they disable or enable the sensor which doesn't stop it from being on or off but stops it from being seen later on in other nodes.
- condition("str"): is 0 when the button isn't affecting a specific sensor and 1 when a button affects this specific sensor.(1/0)
- id(int): is what stays the same throughout as feed value ID changes when deleted and we still need a way to track our devices.


We can move on Sensors RPi which uses feed data alongside with GPIO pin to find the location of a PIR sensor and get input from it.
If there is input: the sensors file checks if adafruit value is the same or different and based on that either uploads a new value to adafruit if it is different or does nothing and after this node gets input, it then gets altered by Buttons RPi. 

Buttons RPi loops through its buttons to find if a button is being pressed or not, then based on input(1/0) it checks if the sensors that are affected by a specific button are disabled or enabled. For example: if the button disables a sensor when pressed it loops through feeds in search for gpio that matches the one it affects and upon finding it checks if its "condition" is 0 which if it is, it changes it and uploads back to adafruit. 

Lastly, LEDs RPi, have counter and total variables which are incremented, if the current sensor condition" is 1 total goes up, otherwise check if the sensor is on
or not and if it is counter and total goes up and if it's off total goes up. Then based on total and counter values led matrix turns the following:
red - all sensors are off or disabled
yellow - at least 1 sensor is on
green - all sensors are on





# Setup Guide:
## Hardware:
- x4 Raspberry Pi 3B+ [Click Me](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/)
- x2 Breadboards,[Click Me](https://uk.rs-online.com/web/p/breadboards/1892277?cm_mmc=UK-PLA-DS3A-_-google-_-CSS_UK_EN_ESD_Control_%26_Cleanroom_%26_PCB_Prototyping_Whoop-_-Breadboards_Whoop+(2)-_-1892277&matchtype=&pla-317955722095&cq_src=google_ads&cq_cmp=11460269911&cq_term=&cq_plac=&cq_net=g&cq_plt=gp&gclid=EAIaIQobChMIhe33gs-1_gIVjMvtCh0eMQNHEAQYAiABEgIIPvD_BwE&gclsrc=aw.ds)
- x3 Buttons [Click Me](https://uk.rs-online.com/web/p/tactile-switches/4791413?cm_mmc=UK-PLA-DS3A-_-google-_-CSS_UK_EN_Switches_Whoop-_-Tactile+Switches_Whoop+(2)-_-4791413&matchtype=&pla-531631261912&cq_src=google_ads&cq_cmp=9771206593&cq_term=&cq_plac=&cq_net=g&cq_plt=gp&gclid=EAIaIQobChMI5b6D6NG1_gIVyuvtCh2sQQYsEAQYASABEgLTnfD_BwE&gclsrc=aw.ds)
- x1 PIR sensor [Click Me](https://uk.farnell.com/mcm/287-18001/sensing-range-max-7m/dp/2830979?gclid=EAIaIQobChMIn_ihrtO1_gIVg_ftCh01AQqSEAYYBSABEgK0TvD_BwE&mckv=_dc|pcrid||plid||kword||match||slid||product|2830979|pgrid||ptaid||&CMP=KNC-GUK-GEN-SHOPPING-PMAX-PrivateLabel-Test990&gross_price=true)
- x1 senseHAT [Click Me](https://uk.farnell.com/raspberry-pi/raspberrypi-sensehat/add-on-board-sense-hat-for-raspberry/dp/2483095?gclid=EAIaIQobChMInMiSz9O1_gIVfIBQBh3SwgS1EAQYASABEgKzsPD_BwE&mckv=_dc|pcrid||plid||kword||match||slid||product|2483095|pgrid||ptaid|&CMP=KNC-GUK-GEN-SHOPPING-PMAX-Medium_ROAS-Test990&gross_price=true)
- x11 Wires [Click Me](https://cpc.farnell.com/pro-signal/psg-jws-65/jumper-wire-set-65pc/dp/PC01769?mckv=s_dc|pcrid|426684131036|kword||match||plid||slid||product|PC01769|pgrid|100371158838|ptaid|pla-960156959477|&CMP=KNC-GUK-CPC-SHOPPING-9262013734-100371158838-PC01769&s_kwcid=AL!5616!3!426684131036!!!network}!960156959477!&gclid=EAIaIQobChMIuojuutK1_gIV0u3tCh3wWA02EAQYBiABEgLudfD_BwE)

3 male to male, 
2 female to female, 
6 male to female.
> Don't forget about monitors, video cables, mice, keyboards, wifi/wireless for the above. 
> If you wish to see Adafruit IO add: an external computer
## Software
 - Install Python [Click Me](https://raspberrytips.com/install-latest-python-raspberry-pi/)
 - Install #commented lines# BEFORE class ...() line in [here](/Resources/). Open terminal, Ctrl + C (copies), Ctrl+Shift+V (pasts), Enter (runs)  
 - Use my or make you're own Adafruit IO key [Click Me](https://learn.adafruit.com/adafruit-io-basics-digital-output/adafruit-io-setup-1)
## Connecting
- Clone GitHub repository [Click Me](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- Set up Creation rpi by opening [create_main.py](/create_main.py/).

- Set up Sensors rpi by opening [sensor_main.py](/sensor_main.py/), then connect PIR as on [photo](/Media/Epic%20Snaget-Jarv.png/) or on [video](/Media/link_to_videos.txt). REMEMBER YOU ARE USING RASPBERRY PI, NOT ARDUINO. INSTEAD OF NUMBERS USE GPIO PINS FOIND [HERE](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png)
- Set up Buttons rpi by opening [button_main.py](/button_main.py/), then connect buttons as on [photo](/Media/Dazzling%20Wluff-Vihelmo%20(1).png/) or on [video](/Media/link_to_videos.txt). REMEMBER YOU ARE USING RASPBERRY PI, NOT ARDUINO. INSTEAD OF NUMBERS USE GPIO PINS FOIND [HERE](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png)


- Set up LEDs RPI by opening [LED main.py](/LED%20main.py/) and by connecting senseHAT to GPIO pins.
- To ***Run***: left click the second icon from the right in Geany OR green "Run" in Thonny. 
- ***Run*** Creation and in the terminal enter: **y**, wait until the code is fully executed and has ended with (code 0)
- ***Run*** Sensors, Buttons, LEDs main. You will see that the LED matrix will change colour to yellow, which shows that it has connected to Adafruit IO successfully.
- If you wave in front of PIR the colour will change to green and you will see **I add things to adafruit** message
- If you disable two sensors by pressing two buttons you will see that matrix changed color to red

## Side notes
- If you wish to add your own devices make sure you input the right parameter in the right place as there are lack of validation in some places which may break the code if exploited.
- You may find that if you run Creation very quickly two times you will find that you've exceeded that amount of adafruit requests [like this](/Media/C83DAEF0-7CBD-40F8-81AA-B246FD53D12B.jpeg)
- If the LED matrix isn't working look [here](https://forums.raspberrypi.com/viewtopic.php?t=192033) for a solution
- If you are having trouble with something else that isn't listed give me an email at: o.kovalchuk@rgu.ac.uk

## How to add stuff to GitHub
How to add to git:
git add *
git commit -m "comment"
git push

ENTER YOUR GITHUB USERNAME
ENTER YOUR GITHUB TOKEN
