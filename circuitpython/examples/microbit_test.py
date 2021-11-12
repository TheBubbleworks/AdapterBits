from microbit import *

print(i2c.scan())

pin1.write_analog(511)
#pin0.set_analog_period(100)
while True:
    adc2 = pin2.read_analog()
    print("P2={}".format(adc2))
    sleep(1000)

