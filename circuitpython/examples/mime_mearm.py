import time
import pwmio
from simpleio import map_range
from analogio import AnalogIn
from adafruit_motor import servo
from picobit import P0, P1, P2, P3, P13, P14, P15, P16, ALL_PINS
import digitalio


# WArning ADC readings are wrong if PicBit USB is connected

if 0:
    dpins = []
    for p in ALL_PINS:
        np = digitalio.DigitalInOut(p)
        np.direction = digitalio.Direction.INPUT
        dpins.append(np)
    print(len(dpins))

    while True:
        for p in dpins:
            print("{}, ".format(p.value), end='')
        print()


base_pwm = pwmio.PWMOut(P13, duty_cycle=2 ** 15, frequency=50)
right_pwm = pwmio.PWMOut(P15, duty_cycle=2 ** 15, frequency=50)
left_pwm = pwmio.PWMOut(P14, duty_cycle=2 ** 15, frequency=50)
grip_pwm = pwmio.PWMOut(P16, duty_cycle=2 ** 15, frequency=50)

base_servo = servo.Servo(base_pwm)
right_servo = servo.Servo(right_pwm)
left_servo = servo.Servo(left_pwm)
grip_servo = servo.Servo(grip_pwm)

a0 = AnalogIn(P0)
a1 = AnalogIn(P1)
a2 = AnalogIn(P2)

button = digitalio.DigitalInOut(P3)

#Base
#{minPulse: 600,  maxPulse: 2400, minAngle: 0,   maxAngle: 179,  currentAngle: 999, pin: AnalogPin.P13, joystick: AnalogPin.P0, direction: 1},

#Right
#{minPulse:  1050, maxPulse: 2400, minAngle: 0,   maxAngle: 135,  currentAngle: 999, pin: AnalogPin.P15, joystick: AnalogPin.P1, direction: 1},

#Left
#{minPulse: 800,  maxPulse: 2100, minAngle: 30,   maxAngle: 160, currentAngle: 999, pin: AnalogPin.P14, joystick: AnalogPin.P2, direction: 1},

#Grip:  = closed, 89 = open
#{minPulse: 1500, maxPulse: 2400, minAngle: 0,   maxAngle: 89,  currentAngle: 999, pin: AnalogPin.P16, joystick: AnalogPin.P3, direction: 1}


class EasingServo:
    def __init__(self, servo, angle, speed):
        self.servo = servo
        self.speed = speed
        self.angle = angle
        self.target_angle = angle

    def target(self, angle):
        self.target_angle = angle

    def update(self):
        self.angle += (self.target_angle - self.angle) * self.speed  # simple easing
        self.servo.angle = self.angle


base = EasingServo(base_servo, 90, 0.1)
left = EasingServo(left_servo, 90, 0.1)
right = EasingServo(right_servo, 90, 0.1)
while True:
    j0 = a0.value
    j1 = a1.value
    j2 = a2.value

    base.target(map_range(j0, 0, 65535-7000, 179, 0))
    base.update()

    right.target(map_range(j1, 0, 65535, 0, 135))
    right.update()

    left.target(map_range(j2, 0, 65535, 30, 160))
    left.update()


    #print(j0, j1, j2)

    #time.sleep(0.01)
    continue

    for angle in range(90, 120, 1):  # 0 - 180 degrees, 5 degrees at a time.
        base_servo.angle = angle
        right_servo.angle = angle
        left_servo.angle = angle
        grip_servo.angle = angle
        time.sleep(0.05)
    for angle in range(120, 90, -1): # 180 - 0 degrees, 5 degrees at a time.
        base_servo.angle = angle
        right_servo.angle = angle
        left_servo.angle = angle
        grip_servo.angle = angle
        time.sleep(0.05)