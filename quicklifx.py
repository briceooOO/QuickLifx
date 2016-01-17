#!/usr/bin/env python
from lifxlan import *
import sys
import time
import random
import requests
import termios, fcntl, sys, os

#Brightness default value
brightnessValue = 32700
#Color defintion
colorIndex=-1
colors = [
		[62978, 65535, brightnessValue, 3500],
		[5525, 65535, brightnessValue, 3500],
		[7615, 65535, brightnessValue, 3500],
		[16173, 65535, brightnessValue, 3500],
		[29814, 65535, brightnessValue, 3500],
		[43634, 65535, brightnessValue, 3500],
		[50486, 65535, brightnessValue, 3500],
		[58275, 65535, brightnessValue, 3500],
		[58275, 0, brightnessValue, 2500],
		[58275, 0, brightnessValue, 5000],
		[58275, 0, brightnessValue, 7500],
		[58275, 0, brightnessValue, 9000]
		]


#Scan lifx bulb (one only)
print("Starting...")
lifx = LifxLAN(1)
print("Ready!")

#Scan keyboard input
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


print("Go!!")
try:
	while 1:
		try:
			c = sys.stdin.read(1)
			if c == 'c':
				colorIndex = (colorIndex + 1) % len(colors)
			if c == 'v':
				if colorIndex > 0:
					colorIndex = colorIndex - 1
				else:
					colorIndex = len(colors) - 1
			if c == 'x':
				brightnessValue = brightnessValue + 500
				if brightnessValue > 65500 :
					brightnessValue = 0
			if c == 'w':
				brightnessValue = brightnessValue - 500
				if brightnessValue < 0 :
					brightnessValue = 65000			
					
			# Print updated color
			colors[colorIndex][2] = brightnessValue
			lifx.set_color_all_lights(colors[colorIndex], 0, True)
			print(colors[colorIndex])
		except IOError: pass
finally:
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

