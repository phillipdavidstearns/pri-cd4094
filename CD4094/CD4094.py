# Abstracts RPi.GPIO functionality to control
# 4094 shiftregister from the 4000 series CMOS logic family
# on Raspberry Pi (tested on RPi 3 B+ and RPi Zero W)
# Requires PRi.GPIO

import RPi.GPIO as GPIO

# This module must be initialized prior to use!
# Example: `CD4094.init( [STROBE, DATA, CLOCK, ENABLE], CHANNELS )`

# global variables for storing pin numbers
STROBE=-1
DATA=-1
CLOCK=-1
ENABLE=-1
CHANNELS=-1

def enable():
	GPIO.output(ENABLE, 1)

def disable():
	GPIO.output(ENABLE, 0)

# Flushes the register by loading with zeros
def clear():
	GPIO.output(DATA, 0)
	for c in range(CHANNELS):
		GPIO.output(CLOCK, 1)
		GPIO.output(CLOCK, 0)
	GPIO.output(STROBE, 1)
	GPIO.output(STROBE, 0)

# Intended to be run prior to program exit.
# Disables output, flushes registers, and stops the GPIO instance
# The module must be reinitialized before next use.
def stop():
	disable()
	clear()
	GPIO.cleanup()

# Accepts a list of boolean or binary values and shifts them
# into the registers.
def update(values):
	for c in range(CHANNELS):
		GPIO.output(DATA, values[CHANNELS - c - 1])
		GPIO.output(CLOCK, 1)
		GPIO.output(CLOCK, 0)
	GPIO.output(STROBE, 1)
	GPIO.output(STROBE, 0)

# Must be run prior to use.
# Sets up the GPIO module, clears the register, and enables output
def init(pins, channels):

	global STROBE
	global DATA
	global CLOCK
	global ENABLE
	global CHANNELS

	# check input values for anomalies
	if len(pins) == 4:
		STROBE, DATA, CLOCK, ENABLE = pins
	else:
		print("[!] Initialization failed.")
		print("[!] Registers require 4 GPIO pins: strobe, data, clock, and enable.")
		return

	if STROBE < 1 or STROBE > 40 or DATA < 1 or DATA > 40 or CLOCK < 1 or CLOCK > 40 or ENABLE < 1 or ENABLE > 40:
		print("[!] Initialization failed.")
		print("[!] GPIO pins must be positive integers from 1-40.")
		return

	if channels is None or type(channels) != int:
		print("[!] Initialization failed.")
		print("[!] Number of channels must be an integer")
		return
	elif channels <= 0:
		print("[!] Initialization failed.")
		print("[!] Number of channels must be greater than 0")
		return
	else:
		CHANNELS = channels
		
	# Setup GPIO instance
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM) # use BCM pin numbers

	# Setup control pins
	for pin in pins: 
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	clear()
	enable()
	print("[+] Initialization succeeded.")
