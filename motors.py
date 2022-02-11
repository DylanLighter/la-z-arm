import smbus
import numpy as np
import time

# setup
bus = smbus.SMBus(1)

addr = 0x40

bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

rangeMin = -180
rangeMax = 180

def rotate(channel, deg):
	channel = 0x06 + channel * 4
	bus.write_word_data(addr, channel, 0)
	signal = deg * 4.6
	bus.write_word_data(addr, channel + 2, int(np.rint(1250 + signal)))

def rotateFinger(index, curl):
	deg = rangeMin + (rangeMax - rangeMin) * (curl / 100)
	rotate(index, deg)
	print(f"rotating {deg} at {curl}% curl")

for i in range(5):
	rotate(i, rangeMin)
