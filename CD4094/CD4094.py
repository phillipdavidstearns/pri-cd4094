# handles input and output for heads-tails related projects
# created to make abstract shiftregister sequential control logic
# also abstracts the hardware based PWM functionality of pigpio

import RPi.GPIO as GPIO

# This module must be initialized prior to use!
# Example: `CD4094.init( [STROBE, DATA, CLOCK, ENABLE], CHANNELS )`

# global variable for storing pin numbers

STROBE=-1
DATA=-1
CLOCK=-1
ENABLE=-1
CHANNELS=-1

def enable():
	GPIO.output(ENABLE, 1)

def disable():
	GPIO.output(ENABLE, 0)

def clear():
	GPIO.output(DATA, 0)
	for c in range(CHANNELS):
		GPIO.output(CLOCK, 0)
		GPIO.output(CLOCK, 1)
	GPIO.output(CLOCK, 0)
	GPIO.output(STROBE, 1)
	GPIO.output(STROBE, 0)

def start():
	clear()
	enable()

def stop():
	disable()
	clear()
	GPIO.cleanup()

# takes a list of boolean values and outputs them
def update(values):
	for c in range(CHANNELS):
		GPIO.output(CLOCK, 0)
		GPIO.output(DATA, values[CHANNELS - c - 1])
		GPIO.output(CLOCK, 1)
	GPIO.output(CLOCK, 0)
	GPIO.output(STROBE, 1)
	GPIO.output(STROBE, 0)
	GPIO.output(DATA, 0)

def init(pins, channels):

	global STROBE
	global DATA
	global CLOCK
	global ENABLE
	global CHANNELS

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM) # use GPIO pin numbers

	# Setup Rregister outputs

	STROBE=pins[0]
	DATA=pins[1]
	CLOCK=pins[2]
	ENABLE=pins[3]
	CHANNELS=channels

	if STROBE == -1 or DATA == -1 or CLOCK == -1 or ENABLE == -1:
		print("Registers require 4 GPIO pins: strobe, data, clock, and enable")
		return

	if CHANNELS == -1:
		print("Number of channels must be greater than 0")
		return

	for pin in pins: 
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	start()