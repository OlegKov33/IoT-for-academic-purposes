import time

from Resources.LEDs import LEDs

led1 = LEDs("name")

# https://forums.raspberrypi.com/viewtopic.php?t=192033
while True:
	led1.process()
