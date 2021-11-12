import time
from busio import I2C
#from bitbangio import I2C
import digitalio
import analogio
import pwmio
import neopixel
from adafruit_motor import servo
from adapterbit import P0, P1, P2, P8, P12, P13, P14, P15, P16, SDA, SCL


# 4tronix lib : https://github.com/oivron/bitbotxl
# PWM:  https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm

# IO conflict on P1 between LightSensorLeft and Servo 1 (so need to deinit pins)
# PWM 5B conflict between P1 (GP27) (SERVO_1))  and P8 (GP11)  LEFT_DIR_PIN

# Add-on card mapping
BUZZER_PIN = P0
LIGHT_SENSOR_LEFT_PIN = P1
LIGHT_SENSOR_RIGHT_PIN = P2

LEFT_SPEED_PIN = P16
LEFT_DIR_PIN = P8
RIGHT_SPEED_PIN = P14
RIGHT_DIR_PIN = P12

SERVO_1_PIN = P1
SERVO_2_PIN = P2

SONAR_TRIG_PIN = P15

NEOPIXEL_PIN = P13
NUM_NEOPIXELS = 12

PCA9557_ADDR  =   0x1c

FORWARD = False
BACKWARD = not FORWARD
STOP = False            # just the way it is...


sonar = digitalio.DigitalInOut(SONAR_TRIG_PIN)

pixels = neopixel.NeoPixel(
    NEOPIXEL_PIN, NUM_NEOPIXELS, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB
)


def test_buzzer():
    buzzer = pwmio.PWMOut(BUZZER_PIN, duty_cycle=0, frequency=440, variable_frequency=True)

    try:
        for f in (262, 294, 330, 349, 392, 440, 494, 523):
            buzzer.frequency = f
            buzzer.duty_cycle = 65535 // 2  # On 50%
            time.sleep(0.02)  # On for 1/4 second
            buzzer.duty_cycle = 0  # Off
            time.sleep(0.01)  # Pause between notes

    finally:
        buzzer.deinit()


def test_sonar():
    while True:
        sonar.direction = digitalio.Direction.OUTPUT
        sonar.value = True
        end_time = time.monotonic_ns() + (10*1000)    # sleep 10 us
        while (time.monotonic_ns()) < end_time:
            pass

        sonar.value = False
        sonar.direction = digitalio.Direction.INPUT
        sonar.pull = digitalio.Pull.UP
        while sonar.value == 0:
            pass
        start_time = time.monotonic_ns()/1000   # time in us
        while sonar.value == 1:
            pass
        end_time = time.monotonic_ns()/1000     # time in us
        elapsed = end_time - start_time
        distance = int(0.01715 * elapsed)
        print("distance = {}".format(distance))


def test_servos():
    servo1_pwm = pwmio.PWMOut(SERVO_1_PIN, duty_cycle=2 ** 15, frequency=50)
    servo2_pwm = pwmio.PWMOut(SERVO_2_PIN, duty_cycle=2 ** 15, frequency=50)

    try:
        servo1 = servo.Servo(servo1_pwm)
        servo2 = servo.Servo(servo2_pwm)

        # Servos
        # https://learn.adafruit.com/circuitpython-essentials/circuitpython-pwm
        # https://learn.adafruit.com/circuitpython-essentials/circuitpython-servo

        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            servo1.angle = angle
            servo2.angle = angle
            time.sleep(0.05)
        for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
            servo1.angle = angle
            servo2.angle = angle
            time.sleep(0.05)
    finally:
        servo1_pwm.deinit()
        servo2_pwm.deinit()


def test_line_sensors():
    # Line sensors

    i2c = I2C(SCL, SDA)

    while not i2c.try_lock():
        pass

    try:
        print([hex(x) for x in i2c.scan()])

        while True:
            i2c.writeto(PCA9557_ADDR, bytes([0x00]))
            time.sleep(0.1)
            result = bytearray(1)
            # ISSUE: https://github.com/adafruit/circuitpython/issues/4082
            # fixed in 7.x (maybe in 6.x, after 6.2.0.rc-0)
            i2c.readfrom_into(PCA9557_ADDR, result)
            line_sensor_left = bool(result[0] & (1 << 0))
            line_sensor_right = bool(result[0] & (1 << 1))
            print("L={}, R={}".format(line_sensor_left, line_sensor_right))
    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c.unlock()


def test_motors():
    # Motors

    left_speed = pwmio.PWMOut(LEFT_SPEED_PIN, frequency=5000, duty_cycle=0)
    left_dir = digitalio.DigitalInOut(LEFT_DIR_PIN)

    right_speed = pwmio.PWMOut(RIGHT_SPEED_PIN, frequency=5000, duty_cycle=0)
    right_dir = digitalio.DigitalInOut(RIGHT_DIR_PIN)

    try:
        left_dir.direction = digitalio.Direction.OUTPUT
        left_speed.duty_cycle = 65535 // 2  # On 50%
        print("Left Motor FORWARD")
        left_dir.value = FORWARD
        time.sleep(1)
        print("Left Motor BACK")
        left_dir.value = BACKWARD
        time.sleep(1)
        left_dir.value = STOP
        left_speed.duty_cycle = 0

        right_dir.direction = digitalio.Direction.OUTPUT
        right_speed.duty_cycle = 65535 // 2  # On 50%
        print("Right Motor FORWARD")
        right_dir.value = FORWARD
        time.sleep(1)
        right_dir.value = BACKWARD
        print("Right Motor BACK")
        time.sleep(1)
        right_dir.value = STOP
        right_speed.duty_cycle = 0

    finally:
        left_dir.deinit()
        left_speed.deinit()
        right_dir.deinit()
        right_speed.deinit()




def test_light_sensors():
# ADC
    light_sensor_left = analogio.AnalogIn(LIGHT_SENSOR_LEFT_PIN)
    light_sensor_right = analogio.AnalogIn(LIGHT_SENSOR_RIGHT_PIN)
    try:
        for i in range(1,50):
            left_sensor = light_sensor_left.value
            right_sensor = light_sensor_right.value
            print("Left={}, right={}".format(left_sensor, right_sensor))
    finally:
        light_sensor_left.deinit()
        light_sensor_right.deinit()

# Neopixels

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return r, g, b


def rainbow_cycle(wait):
    for j in range(2550):
        for i in range(NUM_NEOPIXELS):
            pixel_index = (i * 256 // NUM_NEOPIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def test_neopixels():
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.5)

    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)

    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(0.5)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step


while True:
    test_motors()
    test_buzzer()
    test_servos()
    test_light_sensors()
    test_neopixels()
    test_sonar()
    test_line_sensors()