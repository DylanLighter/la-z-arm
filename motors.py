import smbus
import numpy as np
import time

# setup
bus = smbus.SMBus(1)

addr = 0x40

time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # prescale change
time.sleep(.25)
bus.write_byte_data(addr, 0xfe, 0x79) # set 50Hz
bus.write_byte_data(addr, 0, 0x20)

# set start times to 0
for ch in range(5):
	bus.write_word_data(addr, 0x06 + ch * 4, 0)

rangeMin = -90
rangeMax = 90

def rotate(channel, deg):
	if channel % 2 == 0:
		deg *= -1
	channel = 0x06 + channel * 4
	signal = 59 + deg * 2.3
	bus.write_word_data(addr, channel + 2, int(np.rint(209 + signal)))

def rotateFinger(index, curl):
	if index == 0: # thumb needs to pull half as much
		curl /= 2

	deg = rangeMin + (rangeMax - rangeMin) * (curl / 100)
	rotate(index, deg)
	print(f"rotating {deg} at {curl}% curl")

def resetFingers():
	for i in range(5):
		rotate(i, rangeMin)

resetFingers()
