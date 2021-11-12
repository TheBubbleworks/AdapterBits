import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

from adapterbit import P7, P10

# Release any resources currently in use for the displays
displayio.release_displays()

# 9 is Backlight
tft_cs = P10
tft_dc = P7

# https://learn.adafruit.com/circuitpython-display-support-using-displayio/introduction

#
class Display:

    def __init__(self, spi, width=240, height=240):
        displayio.release_displays()
        self.display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = ST7789(self.display_bus, width=width, height=height, rowstart=80, rotation=180)
        self.display.auto_refresh = False

    def show(self, group):
        self.display.show(group)

    def refresh(self):
        self.display.refresh()

    def splash_screen(self):
        # Make the display context
        splash = displayio.Group(max_size=10)
        self.display.show(splash)

        color_bitmap = displayio.Bitmap(240, 240, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00  # Bright Green

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(200, 200, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xAA0088  # Purple
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
        splash.append(inner_sprite)

        # Draw a label
        text_group = displayio.Group(max_size=10, scale=2, x=50, y=120)
        text = "Hello World!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)