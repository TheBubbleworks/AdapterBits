# Install Circuit Python


## Nano Connect
cp circuitpython/install/nano_rp2040.uf2  /Volumes/RPI-RP2/
cp -r circuitpython/lib/nanobit/*         /Volumes/CIRCUITPY/lib/

## PiPico
cp circuitpython/install/pi_pico.uf2  /Volumes/RPI-RP2/
cp -r circuitpython/lib/picobit/*     /Volumes/CIRCUITPY/lib/


## For all

CPLIB=circuitpython/install/lib
cp -r circuitpython/lib/shared/*   /Volumes/CIRCUITPY/lib/


## Examples

### i2c Scanner

cp circuitpython/examples/i2c_scanner.py /Volumes/CIRCUITPY/code.py


### WaveShare

cp -r ${CPLIB}/adafruit_display_text       /Volumes/CIRCUITPY/lib/
cp ${CPLIB}/adafruit_st7735r.mpy           /Volumes/CIRCUITPY/lib/  
cp circuitpython/examples/waveshare_lcd.py /Volumes/CIRCUITPY/code.py


### Pimoroni EnviroBit

cp ${CPLIB}/adafruit_bme280.mpy                  /Volumes/CIRCUITPY/lib/
cp ${CPLIB}/adafruit_tcs34725.mpy                /Volumes/CIRCUITPY/lib/
cp circuitpython/examples/pimoroni_envirobit.py  /Volumes/CIRCUITPY/code.py  


### Kitronik GameZip

cp ${CPLIB}/neopixel.mpy /Volumes/CIRCUITPY/lib/adafruit_neopixel.mpy
cp circuitpython/examples/kitronik_gamezip_pong.py /Volumes/CIRCUITPY/code.py


### Kitronik Piano

- TODO: REVISIT
cp circuitpython/examples/kitronik_piano.py /Volumes/CIRCUITPY/code.py
cp circuitpython/examples/klef-piano.py /Volumes/CIRCUITPY/code.py




### Pimoroni ScrollBit
cp circuitpython/examples/pimoroni_scrollbit_helloworld.py  /Volumes/CIRCUITPY/code.py  


### Pimoroni NoiseBit

cp circuitpython/examples/pimoroni_noisebit.py  /Volumes/CIRCUITPY/code.py  


### Pimoroni TouchBit

#### Simple
cp circuitpython/examples/pimoroni_touchbit_simple.py  /Volumes/CIRCUITPY/code.py

#### HID

cp -r ${CPLIB}/adafruit_hid            /Volumes/CIRCUITPY/lib/ 
cp circuitpython/examples/pimoroni_touchbit_hid_keyboard.py  /Volumes/CIRCUITPY/code.py  


### Protopic Simon Says

cp circuitpython/examples/protopic_simonsays.py  /Volumes/CIRCUITPY/code.py



### 4Tronix BitBotXL

cp -r ${CPLIB}/adafruit_motor /Volumes/CIRCUITPY/lib/
rm /Volumes/CIRCUITPY/lib/neopixel.py               # ensure we use the correct lib
cp ${CPLIB}/neopixel.mpy /Volumes/CIRCUITPY/lib/
cp circuitpython/examples/4tronix_bitbotxl.py /Volumes/CIRCUITPY/code.py


### Mime - MeArm


cp -r ${CPLIB}/simpleio.mpy   /Volumes/CIRCUITPY/lib/
cp -r ${CPLIB}/adafruit_motor /Volumes/CIRCUITPY/lib/

cp circuitpython/examples/mime_mearm.py /Volumes/CIRCUITPY/code.py


### Tracker

Uses:
    Pimoroni Pirate Audio
    Pimoroni Piano Hat (Framboisdorf)
    Pimeroni HAcker Hat
    4Tronix bit:2:pi

Pinout
    P0      11  
    P1      35
    P2      40
    P8      22

    P7      21
    P9      
    P10     24


cp -r ${CPLIB}/adafruit_display_shapes /Volumes/CIRCUITPY/lib/
cp -r ${CPLIB}/adafruit_display_text   /Volumes/CIRCUITPY/lib/
cp -r ${CPLIB}/adafruit_imageload      /Volumes/CIRCUITPY/lib/
cp    ${CPLIB}/adafruit_st7789.mpy     /Volumes/CIRCUITPY/lib/

cp -r circuitpython/examples/tracker/lib/*    /Volumes/CIRCUITPY/lib/
cp -r circuitpython/examples/tracker/assets   /Volumes/CIRCUITPY/
cp    circuitpython/examples/tracker/code.py  /Volumes/CIRCUITPY/

