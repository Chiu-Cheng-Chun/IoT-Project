import pigpio
import time
 
PWM_CONTROL_PIN_1 = 18
PWM_CONTROL_PIN_2 = 12
PWM_FREQ = 50
STEP = 100000
 
pi = pigpio.pi()
 
try:
    print('Press Ctrl-C to stop')
    while True:
        print('Clockwise')
        pi.write(PWM_CONTROL_PIN_2, 0)
        for speed in range(0, 1000001, STEP):
            print('Work Cycle={: >6}'.format(speed))
            pi.hardware_PWM(PWM_CONTROL_PIN_1, PWM_FREQ, speed)
            time.sleep(2)
        for speed in range(1000000, -1, -STEP):
            print('Work Cycle={: >6}'.format(speed))
            pi.hardware_PWM(PWM_CONTROL_PIN_1, PWM_FREQ, speed)
            time.sleep(2)
        print('CounterClockwise')
        pi.write(PWM_CONTROL_PIN_1, 0)
        for speed in range(0, 1000001, STEP):
            print('Work Cycle={: >6}'.format(speed))
            pi.hardware_PWM(PWM_CONTROL_PIN_2, PWM_FREQ, speed)
            time.sleep(2)
        for speed in range(1000000, -1, -STEP):
            print('Work Cycle={: >6}'.format(speed))
            pi.hardware_PWM(PWM_CONTROL_PIN_2, PWM_FREQ, speed)
            time.sleep(2)
except KeyboardInterrupt:
    print('\nClose Program')
finally:
    pi.set_mode(PWM_CONTROL_PIN_1, pigpio.INPUT)
    pi.set_mode(PWM_CONTROL_PIN_2, pigpio.INPUT)
