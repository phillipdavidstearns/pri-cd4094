import pigpio
import logging

################################################################
# CLASS DEFINITION: CD4094

class CD4094():
  def __init__(self, pins=[17,27,22,23], channels=8):
    logging.info('[CD4094] Initializing new CD4094 instance.')
    logging.debug('[CD4094] Spinning up pigpio instance.')
    self.pi = pigpio.pi()
    self.pins = pins

    if len(self.pins) == 4:
      self.strobePin, self.dataPin, self.clockPin, self.enablePin = self.pins
    else:
      raise Exception('pins argument expects a list of 4 GPIO pins: strobe, data, clock, and enable.')

    if self.strobePin < 1 or self.strobePin > 40 or self.dataPin < 1 or self.dataPin > 40 or self.clockPin < 1 or self.clockPin > 40 or self.enablePin < 1 or self.enablePin > 40:
      raise Exception('GPIO pins must be positive integers from 1-40.')

    if channels is None or type(channels) != int:
      raise Exception('channels must be an integer')

    if channels <= 0:
      raise Exception('channels must be greater than 0')

    self.channels = channels

    #logging.debug('[CD4094] Initializing pins.')
    for pin in self.pins:
      self.pi.set_mode(pin, pigpio.OUTPUT)
      self.pi.write(pin, 0)
    self.reset()
    self.enable()

  def enable(self):
    #logging.debug('[CD4094] Enabling output.')
    self.pi.write(self.enablePin, 1)

  def disable(self):
    #logging.debug('[CD4094] Disabling output.')
    self.pi.write(self.enablePin, 0)

  def reset(self):
    #logging.debug('[CD4094] Resetting state.')
    self.pi.write(self.dataPin, 0)
    for i in range(self.channels):
      self.pi.write(self.clockPin, 1)
      self.pi.write(self.clockPin, 0)
    self.pi.write(self.strobePin, 1)
    self.pi.write(self.strobePin, 0)

  def update(self, data: int):
    #logging.debug('[CD4094] Updating state: %s' % repr(data))
    for i in range(self.channels):
      try:
        bit = data >> (self.channels -1 - i) & 0b1
      except:
        bit = 0
      self.pi.write(self.dataPin, bit)
      self.pi.write(self.clockPin, 1)
      self.pi.write(self.clockPin, 0)
    self.pi.write(self.strobePin, 1)
    self.pi.write(self.strobePin, 0)

  def stop(self):
    logging.info('[CD4094] Stopping.')
    self.disable()
    self.reset()