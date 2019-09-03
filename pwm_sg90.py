import RPi.GPIO as GPIO
import time
 
CONTROL_PIN = 17
PWM_FREQ = 50
STEP=180
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
 
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
 
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle
 
try:
    print('Press Ctrl-C to stop!')
    while(1):
        for angle in range(0, 181, STEP):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            print('Angle={: >3}, Work Cycle={:.2f}'.format(angle, dc))
	    time.sleep(0.5)

except KeyboardInterrupt:
    print('Close Process!')
