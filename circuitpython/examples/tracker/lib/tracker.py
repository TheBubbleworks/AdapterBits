import displayio
import terminalio
from adafruit_display_text import label
import adafruit_imageload
from adafruit_display_shapes.rect import Rect

# -----




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
        dim1, dim2 = (self.pattern_cols, self.pattern_rows)
        self.note_grid = [[0 for i in range(dim1)] for j in range(dim2)]
        print(self.note_grid)
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
        self.beatmarker_group.y = 32
        self.beatmarker_group.append(self.beatmarker)



        # Draw a label
        self.title_group = displayio.Group(x=0, y=0)
        self.text_area = label.Label(terminalio.FONT, text="PicoTracker", color=0xFFFF00, scale=2)
        self.text_area.anchor_point=(0.5, 0)
        self.text_area.anchored_position=(int(self.screen_width/2), 0)

        self.title_group.append(self.text_area)  # Subgroup for text scaling

        self.group = displayio.Group()
        self.group.append(self.pattern_group)
        self.group.append(self.beatmarker_group)
        self.group.append(self.title_group)

    def tick(self):
        self.send_events()
        self.beat_marker_last_col = self.beat_marker_col
        self.beat_marker_col = (self.beat_marker_col + 1) % self.pattern_cols
        self.beatmarker_group.x = self.beat_marker_col * TrackerScreen.CELL_WIDTH

    def send_events(self):
        x = self.beat_marker_col
        for y in range(0, self.pattern_rows):
            marker_id = self.pattern_grid[x, y]
            if marker_id != TrackerScreen.EMPTY_CELL:
                self.event_handler(1, x, y, marker_id, self.note_grid[x][y])

    def add_marker(self, x, y, marker_id):
        self.pattern_grid[x, y] = marker_id

    def add_note(self, x, y, note):
        self.note_grid[x][y] = note

    def add_now(self, y, marker_id, note):
        self.add_note(self.beat_marker_col, y, note)
        self.add_marker(self.beat_marker_col, y, marker_id)




