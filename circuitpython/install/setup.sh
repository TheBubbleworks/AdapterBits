
# The commands to download and create this install folder.
# Records the versions of the CircuitPython firmwares and libraries used.

cd circuitpython/install
wget https://adafruit-circuit-python.s3.amazonaws.com/bin/raspberry_pi_pico/en_GB/adafruit-circuitpython-raspberry_pi_pico-en_GB-7.0.0-alpha.6.uf2 -O pi_pico.uf2
wget https://adafruit-circuit-python.s3.amazonaws.com/bin/arduino_nano_rp2040_connect/en_GB/adafruit-circuitpython-arduino_nano_rp2040_connect-en_GB-7.0.0-alpha.6.uf2 -O nano_rp2040.uf2
wget https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20210818/adafruit-circuitpython-bundle-7.x-mpy-20210818.zip
#Source for ref only:
#wget https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20210818/adafruit-circuitpython-bundle-py-20210818.zip
unzip adafruit-circuitpython-bundle-7.x-mpy-20210818.zip
mv adafruit-circuitpython-bundle-7.x-mpy-20210818/lib .
rm -fr adafruit-circuitpython-bundle-7.x-mpy-20210818*
