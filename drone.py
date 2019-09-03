# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:13:10 2019

@author: craig
"""
import spidev
import time
import RPi.GPIO as GPIO
import pigpio

PWM_CONTROL_PIN_4 = 18
CONTROL_PIN_4 = 12
PWM_FREQ = 50
pi = pigpio.pi()

GPIO.setmode(GPIO.BOARD) #使用板上定義的腳位號碼
GPIO.setup(35, GPIO.OUT) #將35設為輸出
GPIO.setup(40, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vry_channel = 1
vrx_channel = 2

# Define delay between readings (s)
delay = 0.5

while True:

  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)

  # Read switch state
  swt_val = ReadChannel(swt_channel)

  # Print out results
  print("--------------------------------------------" )
  print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
  if vrx_pos < 50:
      GPIO.output(35, True)
      print("Go forward! ")
      print( "Motor1:", 350000, "Motor2:", 350000)
      print( "Motor3:", 500000, "Motor4:", 500000)
      pi.write(CONTROL_PIN_4, 0)
      pi.hardware_PWM(PWM_CONTROL_PIN_4, PWM_FREQ, 500000)
  if vrx_pos < 550 and vry_pos > 950:
      GPIO.output(40, True)
      print("Go left! ")
      print( "Motor1:", 350000, "Motor2:", 500000)
      print( "Motor3:", 350000, "Motor4:", 500000)
  if vrx_pos > 950 and vry_pos < 550:
      GPIO.output(36, True)
      print("Go back! ")
      print( "Motor1:", 500000, "Motor2:", 500000)
      print( "Motor3:", 350000, "Motor4:", 350000)
  if vrx_pos < 550 and vry_pos < 50:
      GPIO.output(38, True)
      print("Go right! ")
      print( "Motor1:", 500000, "Motor2:", 350000)
      print( "Motor3:", 500000, "Motor4:", 350000)

  # Wait before repeating loop
  time.sleep(delay)
  GPIO.output(35, False)
  GPIO.output(40, False)
  GPIO.output(36, False)
  GPIO.output(38, False)
  pi.hardware_PWM(PWM_CONTROL_PIN_4, PWM_FREQ, 0)

pi.hardware_PWM(PWM_CONTROL_PIN_4, PWM_FREQ, 0)
pi.set_mode(PWM_CONTROL_PIN_4, pigpio.INPUT)
