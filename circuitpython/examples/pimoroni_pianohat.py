import time
import board
import busio
from adafruit_cap1188.i2c import CAP1188_I2C
from picobit import SCL, SDA

i2c = busio.I2C(SCL, SDA)

while not i2c.try_lock():
    pass

try:
    print([hex(x) for x in i2c.scan()])

    cap1 = CAP1188_I2C(i2c, 0x28)
    cap2 = CAP1188_I2C(i2c, 0x2b)

    while True:
        for i in range(1, 9):
            if cap1[i].value:
                print("Cap1 Pin {} touched!".format(i))
        for i in range(1, 9):
            if cap2[i].value:
                print("Cap2 Pin {} touched!".format(i))

        time.sleep(0.01)

finally:
    i2c.unlock()



