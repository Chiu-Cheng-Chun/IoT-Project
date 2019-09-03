import pigpio
import time

PWM_LED_PIN = 18
PWM_FREQ = 800

pi = pigpio.pi()

try:
	print('Press Ctrl-C to stop')
	while True:
		for i in range(0,30,1):
			pi.hardware_PWM(PWM_LED_PIN, PWM_FREQ, i*10000)
			time.sleep(0.1)
                for i in range(29,-1,-1):
                        pi.hardware_PWM(PWM_LED_PIN, PWM_FREQ, i*10000)
                        time.sleep(0.1)
except KeyboardInterrupt:
	print('\nClose Program')
finally:
	pi.set_mode(PWM_LED_PIN, pigpio.INPUT)
