from Resources.Adafruit import Adafruit
ada = Adafruit("name")

#ada.clearAll()
temp = str(input("Do you have a preset?(y/n): "))
temp2 = -1
if temp == "y":
	ada.preset()
else:
	while temp2  <0:
		temp2 = int(input("Enter a number of devices that you have: "))

for x in range (temp2):
	ada.create()
