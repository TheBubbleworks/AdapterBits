
# Pico C Examples


Ensure you have setup the Raspberry Pi Pico SDK first.   

These examples assumes it's been installed into:  `~/pico/pico-sdk`


## SPI Display (ST7735) - PIO

This example is based on code from [REF] and displays colour bars.
The SPI communication is performed via PIO.

```
export PICO_SDK_PATH=~/pico/pico-sdk
cd c/examples/spi_display
mkdir build
cd build
cmake ..
make -j
cp spi_display.uf2 /Volumes/RPI-RP2/
```



## SPI Display (ST7735) - Pico SPI API

TODO: https://github.com/bablokb/pico-st7735


