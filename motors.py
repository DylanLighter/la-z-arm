#!/usr/bin/env python3

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
for ch in range(16):
	bus.write_word_data(addr, 0x06 + ch * 4, 0)

rangeMin = -90
rangeMax = 90

def rotate(channel, deg):
	# Odd finger motors flip rotation
	if channel < 5 and channel % 2 == 0:
		deg *= -1
	channel = 0x06 + channel * 4
	signal = 59 + deg * 2.3
	bus.write_word_data(addr, channel + 2, int(np.rint(209 + signal)))

def rotateJoint(index, curl):
	deg = rangeMin + (rangeMax - rangeMin) * (curl / 100)
	rotate(index, deg)
	print(f"rotating {deg} at {curl}% curl")

def resetMotors():
	for i in range(16):
		rotate(i, rangeMin)

resetMotors()

if __name__ == "__main__":
	print("==Manual motor control==")
	print("i [channel] - select channel")
	print("[# degrees] - rotate current motor")
	print("Enter nothing to exit")
	currCh = 0
	while True:
		command = input()
		if command == "":
			resetMotors()
			break
		elif command.startswith("i") and command[2:].isnumeric():
			currCh = int(command[2:])
		elif command.isnumeric():
			rotate(currCh, int(command))
		else:
			print("Invalid command.")
