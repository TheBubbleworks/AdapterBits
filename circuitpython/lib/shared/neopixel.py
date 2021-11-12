import adafruit_neopixel

class NeoPixel(adafruit_neopixel.NeoPixel):

    # TODO: revisit this signature, make it match Microbit API
    def __init__(
        self, pin, n, bpp=3, brightness=1.0, auto_write=False, pixel_order=None
    ):
        # get to the raw Circuit Python pin underneath
        pin = pin.pin
        super().__init__(pin, n, bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)

    def clear(self):
        self.fill(0)
