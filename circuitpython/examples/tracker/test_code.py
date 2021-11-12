import time
import busio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import adafruit_imageload
from adafruit_display_shapes.rect import Rect

from picobit import P7, P10, SCK, MOSI

(SCREEN_WIDTH, SCREEN_HEIGHT) = (240, 240)

displayio.release_displays()
spi = busio.SPI(SCK, MOSI)
display_bus = displayio.FourWire(spi, command=P7, chip_select=P10)
display = ST7789(display_bus, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                 rowstart=80, rotation=180)

display.auto_refresh = False


# -----

text = "PicoTracker"
font = terminalio.FONT
color = 0x7F0000
text_area = label.Label(font, text=text, color=color, scale=3)
text_area.x = 20
text_area.y = 12
#pattern_group.append(text_area)


class TrackerScreen:

    CELL_WIDTH = 16
    CELL_HEIGHT = 16

    EMPTY_CELL = 0
    BEAT_MARKER_CELL = 24

    def __init__(self, screen_width=240, screen_height=240):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pattern_cols = int(self.screen_width / TrackerScreen.CELL_WIDTH)
        self.pattern_rows = int(self.screen_height / TrackerScreen.CELL_HEIGHT)

        self.event_handler = lambda w,x,y,z: None

        self.sprite_sheet, self.palette = adafruit_imageload.load("assets/icons/icons.bmp",
                                                        bitmap=displayio.Bitmap,
                                                        palette=displayio.Palette)

        self.pattern_grid = displayio.TileGrid(self.sprite_sheet,
                                          x=0,
                                          y=32,
                                          pixel_shader=self.palette,
                                          width=self.pattern_cols * TrackerScreen.CELL_WIDTH,
                                          height=self.pattern_rows * TrackerScreen.CELL_HEIGHT,
                                          tile_width=TrackerScreen.CELL_WIDTH,
                                          tile_height=TrackerScreen.CELL_HEIGHT)

        self.pattern_group = displayio.Group()
        self.pattern_group.append(self.pattern_grid)
        self.beat_marker_col = 0
        self.beat_marker_last_col = 0
        self.beat_marker_line_pos = self.beat_marker_col

        # Beet marker overlay
        self.beatmarker = Rect(0, 0,
                               TrackerScreen.CELL_WIDTH, self.screen_height,
                               outline=0xffff00, fill=None)

        self.beatmarker_group = displayio.Group()
        self.beatmarker_group.append(self.beatmarker)

        self.group = displayio.Group()
        self.group.append(self.pattern_group)
        self.group.append(self.beatmarker_group)

    def tick(self):
        self.beatmarker_group.x = self.beat_marker_col * TrackerScreen.CELL_WIDTH
        self.beat_marker_last_col = self.beat_marker_col
        self.beat_marker_col = (self.beat_marker_col + 1) % self.pattern_cols
        self.send_events()

    def send_events(self):
        col = self.beat_marker_col
        for row in range(1, self.pattern_rows):
            marker_id = self.pattern_grid[row, col]
            if marker_id != TrackerScreen.EMPTY_CELL:
                self.event_handler(1, row, col, marker_id)

    def add_marker(self, row, col, marker_id):
        self.pattern_grid[row, col]= marker_id

    def add_now(self, row, marker_id):
        self.add_marker(row, self.beat_marker_col, marker_id)



while True:
    tracker_screen.tick()
    time.sleep(0.25)
    display.refresh()



