# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio
and draw a solid red background
"""

# cp -r picobit/pi_pico/libraries/adafruit-circuitpython-bundle-6.x-mpy-20210405/lib/adafruit_st7735r.mpy /Volumes/CIRCUITPY
# cp -r picobit/pi_pico/libraries/adafruit-circuitpython-bundle-6.x-mpy-20210405/lib/adafruit_display_text /Volumes/CIRCUITPY
# cp picobit/pi_pico/examples/waveshare_lcd.py /Volumes/CIRCUITPY/code.py
import board
import busio
import displayio
import terminalio

from adafruit_st7735r import ST7735R
from adafruit_display_text import label

# Release any resources currently in use for the displays
displayio.release_displays()

from adapterbit import P8, P12, P16, MISO, MOSI, SCK

TFT_CS = P16  # Chip select control pin
TFT_DC = P12  # Data Command control pin
TFT_RST= P8   # Reset pin (could connect to RST pin)
#TFT_BL  = P1



spi = busio.SPI(SCK, MOSI=MOSI, MISO=MISO)

display_bus = displayio.FourWire(
    spi, command=TFT_DC, chip_select=TFT_CS, reset=TFT_RST
)

display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True)


# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(150, 118, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=2, x=11, y=64)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)


while True:
    pass
