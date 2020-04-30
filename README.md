# rpi-cd4094

An RPi.GPIO wrapper that simplifies controlling CD4094 CMOS 8-bit latched shift registers from a Raspberry Pi

## Installation

1. `$ sudo apt-get update; sudo apt-get install git`
1. `$ git clone https://github.com/phillipdavidstearns/rpi-cd4094.git`
1. `$ cd rpi-cd4094`
1. `$ sudo python3 setup.py install`

## Usage

```python
import CD4094

# setup pins using BCM GPIO pin numbers
STROBE = 17 # latch strobe GPIO pin
DATA = 27 # data GPIO pin
CLOCK = 22 # clock GPIO pin
ENABLE = 23 # enable GPIO pin

#specify number of channels in the shift register chain
CHANNELS = 32 # 

#bundle pins
PINS = [STROBE, DATA, CLOCK, ENABLE]

#initializes RPi.GPIO instance
CD4094.init(PINS, CHANNELS)

# toggle output
CD4094.enable()
CD4094.disable()

# flush register
CD4094.clear()

# pre-exit RPi.GPIO cleanup
CD4094.stop()

# shift data into register
CD4094.update(list) # list of boolean values to output
```
