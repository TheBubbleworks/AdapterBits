import time
import math
import busio
import digitalio
import analogio
import adafruit_bme280
import Adafruit_TCS34725
from adapterbit import SCL, SDA, P2, P8

led = digitalio.DigitalInOut(P8)
led.direction = digitalio.Direction.OUTPUT

mic = analogio.AnalogIn(P2)

i2c = busio.I2C(SCL, SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
tcs = Adafruit_TCS34725.TCS34725(i2c)



# BME280 Pressure Sensor

bme280.sea_level_pressure = 1030

b = 17.62
c = 243.12
gamma = (b * bme280.temperature /(c + bme280.temperature)) + math.log(bme280.humidity / 100.0)
dewpoint = (c * gamma) / (b - gamma)

print("\nTemperature: %0.1f C" % bme280.temperature)
print("Humidity: %0.1f %%" % bme280.humidity)
print("Pressure: %0.1f hPa" % bme280.pressure)
print("Altitude = %0.2f meters" % bme280.altitude)
print("Dewpoint", dewpoint)



# TCS  Light Sensor

led.value = True

tcs.interrupt = False
# Read the R, G, B, C color data.
r, g, b,c  = tcs.color_raw

# Calculate color temperature using utility functions.  You might also want to
# check out the colormath library for much more complete/accurate color functions.
color_temp = tcs.color_temperature

# Calculate lux with another utility function.
lux = tcs.lux

# Print out the values.
print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))

# Print out color temperature.
if color_temp is None:
    print('Too dark to determine color temperature!')
else:
    print('Color Temperature: {0} K'.format(color_temp))

# Print out the lux.
print('Luminosity: {0} lux'.format(lux))

# Enable interrupts and put the chip back to low power sleep/disabled.
tcs.active = False
led.value = False


while True:
    sample = mic.value
    print(sample)