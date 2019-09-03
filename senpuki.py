#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import queue
import RPi.GPIO as GPIO
import pigpio
import time

sq = queue.Queue()
rq = queue.Queue()
s = 0
r = 0
 
#GPIO.setmode(GPIO.BOARD) #使用板上定義的腳位號碼
PWM_CONTROL_PIN_1 = 18
PWM_CONTROL_PIN_2 = 12
PWM_FREQ = 50

pi = pigpio.pi()

#--------sg90---------
CONTROL_PIN = 11
STEP=180
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
pwm = GPIO.PWM(CONTROL_PIN, 25)
pwm.start(0)
#---------------------

# 持續獲取使用者輸入
def get_input(sq, rq):
    while(1):
        try:
            rotating_speed, rotating = input("請輸入風速及是否旋轉(轉速為0~3，旋轉為1，不旋轉為0\n").split(",")
            rotating_speed = int(rotating_speed)
            rotating = int(rotating)
            if 0<=rotating_speed<=3 and 0<=rotating<=1 and str(rotating_speed).isdigit() and str(rotating).isdigit():
                print("轉速為:", rotating_speed, "旋轉狀況為:", rotating, "\n")
                sq.put(rotating_speed)
                rq.put(rotating)
            elif rotating_speed == 5 and rotating == 5 and str(rotating_speed).isdigit() and str(rotating).isdigit():
                print("終止設定!\n")
                break
            else:
                print("輸入格式有誤!\n")
        except:
            print("輸入格式有誤\n")

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

#控制sg90
def sg90_controll(rq):
    signal2 = 0
    while(1):
        if rq.empty() == False:
            signal2 = rq.get()
        if signal2 == 1:
            for angle in range(0, 181, STEP):
                dc = angle_to_duty_cycle(angle)
                pwm.ChangeDutyCycle(dc)
                time.sleep(1)

#控制DC_motor
def dc_motor_control(sq):
    rotate_speed = 300000
    signal1 = 0
    pi.write(PWM_CONTROL_PIN_2, 0)
    while(1):
        if sq.empty() == False:
            signal1 = sq.get()
        pi.hardware_PWM(PWM_CONTROL_PIN_1, PWM_FREQ, rotate_speed*signal1)
 
# 產生線程
try:
   t1 = threading.Thread(target=get_input, args=[sq, rq])
   t2 = threading.Thread(target=sg90_controll, args=[rq])
   t3 = threading.Thread(target=dc_motor_control, args=[sq])
   t1.start()
   t2.start()
   t3.start()
 
except:
   print ("Error: unable to start thread")
 
finally:
    pi.set_mode(PWM_CONTROL_PIN_1, pigpio.INPUT)
    pi.set_mode(PWM_CONTROL_PIN_2, pigpio.INPUT)
