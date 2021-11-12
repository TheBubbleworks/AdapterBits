
# CircuitPython built-in classes
import time
import digitalio
import analogio
import pwmio
from busio import I2C
#from bitbangio import I2C
import adapterbit


# Facade/wrapper classes


class PinFacade:

    PULL_UP = digitalio.Pull.UP
    PULL_DOWN = digitalio.Pull.DOWN

    def __init__(self, pin):
        self.pin = pin
        self._is_setup = False
        self._digital = None
        self._analog_in = None
        self._analog_out = None

    # Analog out pin handling
    # https://microbit-micropython.readthedocs.io/en/v1.0.1/pin.html#microbit.MicroBitAnalogDigitalPin
    # 0-1023
    def write_analog(self, value):
        # if self._digital is not None:
        #     self._digital.deinit()
        #     self._digital = None

        if not self._is_setup:
            self._analog_out = pwmio.PWMOut(self.pin, duty_cycle=value, frequency=50, variable_frequency=True)
            self._is_setup = True

        if not self._analog_out:
            raise Exception("Pin setup to be something other than analog out")

        self._analog_out.duty_cycle = value * int(65535/1023)

    # 1-1000
    def set_analog_period(self, period_ms):
        # if not self._is_setup:
        #     self._analog_out = pwmio.PWMOut(self.pin, duty_cycle=value, frequency=50, variable_frequency=True)

        if not self._analog_out:
            raise Exception("Pin setup to be something other than analog out")

        self._analog_out.frequency = int(1000/period_ms)



    def read_analog(self):
        if not self._is_setup:
            self._analog_in = analogio.AnalogIn(self.pin)
            self._is_setup = True

        if not self._analog_in:
            raise Exception("Pin setup to be something other than analog in")

        return self._analog_in.value


    # Digital pin handling

    def read_digital(self):
        if not self._is_setup:
            self._digital = digitalio.DigitalInOut(self.pin)
            self._digital.direction = digitalio.Direction.INPUT
            self._is_setup = True

        if not self._digital:
            raise Exception("Pin setup to be something other than digital")


        return self._digital.value

    def write_digital(self, value):
        if not self._is_setup:
            self._digital = digitalio.DigitalInOut(self.pin)
            self._digital.direction = digitalio.Direction.OUTPUT
            self._is_setup = True

        if not self._digital:
            raise Exception("Pin setup to be something other than digital")

        self._digital.value = value


    def set_pull(self, dir):
        if not self._is_setup:
            self._digital = digitalio.DigitalInOut(self.pin)
            self._digital.direction = digitalio.Direction.INPUT
            self._is_setup = True

        if not self._digital:
            raise Exception("Pin setup to be something other than digital")

        self._digital.pull = dir



# https://microbit-micropython.readthedocs.io/en/v1.0.1/i2c.html

class I2CFacade:

    def __init__(self):
        self.i2c = None

    def _check_init(self):
        if self.i2c is None:
            self.i2c = I2C(adapterbit.SCL, adapterbit.SDA)

        self.i2c.unlock()

        while not self.i2c.try_lock():
            pass

    def scan(self):
        self._check_init()

        try:
            return [hex(x) for x in self.i2c.scan()]
        finally:
            self.i2c.unlock()

    # write array.  TODO:  repeat is ignored
    # TODO: Locking
    def write(self, address, buf, repeat=False):
        self._check_init()
        self.i2c.writeto(address, bytes(buf))
        #print("TODO: revist i2c delay")
        time.sleep(0.01)

    # fixed in 7.x (maybe in 6.x, after 6.2.0.rc-0)
    # TODO: Locking
    def read(self, address, size, repeat=False):
        self._check_init()
        result = bytearray(size)
        self.i2c.readfrom_into(address, result)
        print("TODO: revist i2c delay")
        time.sleep(0.1)
        return result


# Stub classes, no replacement functionality to implement a proper facade/wrapper class

class DisplayStub:

    def scroll(self, message, wait=True, loop=False):
        print("Display.scroll:{}".format(message))

    def set_pixel(self, x, y, value):
        print("Display.set_pixel:{},{}={}".format(x, y, value))

    def show(self, pattern):
        print("Display.show:{}".format(pattern))

class Image:

    def __init__(self, bits):
        pass

    def get_pixel(self, x, y):
        return 1

class ImageImpl(Image):


    HEART = Image(
        '09090:'
        '99999:'
        '99999:'
        '09990:'
        '00900:'
    )
    HEART_SMALL = Image(
        '00000:'
        '09090:'
        '09990:'
        '00900:'
        '00000:'
    )
    HAPPY = Image(
        '00000:'
        '09090:'
        '00000:'
        '90009:'
        '09990:'
    )
    SMILE = Image(
        '00000:'
        '00000:'
        '00000:'
        '90009:'
        '09990:'
    )
    SAD = Image(
        '00000:'
        '09090:'
        '00000:'
        '09990:'
        '90009:'
    )
    CONFUSED = Image(
        '00000:'
        '09090:'
        '00000:'
        '09090:'
        '90909:'
    )
    ANGRY = Image(
        '90009:'
        '09090:'
        '00000:'
        '99999:'
        '90909:'
    )
    ASLEEP = Image(
        '00000:'
        '99099:'
        '00000:'
        '09990:'
        '00000:'
    )
    SURPRISED = Image(
        '09090:'
        '00000:'
        '00900:'
        '09090:'
        '00900:'
    )
    SILLY = Image(
        '90009:'
        '00000:'
        '99999:'
        '00909:'
        '00999:'
    )
    FABULOUS = Image(
        '99999:'
        '99099:'
        '00000:'
        '09090:'
        '09990:'
    )
    MEH = Image(
        '09090:'
        '00000:'
        '00090:'
        '00900:'
        '09000:'
    )
    YES = Image(
        '00000:'
        '00009:'
        '00090:'
        '90900:'
        '09000:'
    )
    NO = Image(
        '90009:'
        '09090:'
        '00900:'
        '09090:'
        '90009:'
    )
    CLOCK12 = Image(
        '00900:'
        '00900:'
        '00900:'
        '00000:'
        '00000:'
    )
    CLOCK1 = Image(
        '00090:'
        '00090:'
        '00900:'
        '00000:'
        '00000:'
    )
    CLOCK2 = Image(
        '00000:'
        '00099:'
        '00900:'
        '00000:'
        '00000:'
    )
    CLOCK3 = Image(
        '00000:'
        '00000:'
        '00999:'
        '00000:'
        '00000:'
    )
    CLOCK4 = Image(
        '00000:'
        '00000:'
        '00900:'
        '00099:'
        '00000:'
    )
    CLOCK5 = Image(
        '00000:'
        '00000:'
        '00900:'
        '00090:'
        '00090:'
    )
    CLOCK6 = Image(
        '00000:'
        '00000:'
        '00900:'
        '00900:'
        '00900:'
    )
    CLOCK7 = Image(
        '00000:'
        '00000:'
        '00900:'
        '09000:'
        '09000:'
    )
    CLOCK8 = Image(
        '00000:'
        '00000:'
        '00900:'
        '99000:'
        '00000:'
    )
    CLOCK9 = Image(
        '00000:'
        '00000:'
        '99900:'
        '00000:'
        '00000:'
    )
    CLOCK10 = Image(
        '00000:'
        '99000:'
        '00900:'
        '00000:'
        '00000:'
    )
    CLOCK11 = Image(
        '09000:'
        '09000:'
        '00900:'
        '00000:'
        '00000:'
    )
    ARROW_N = Image(
        '00900:'
        '09990:'
        '90909:'
        '00900:'
        '00900:'
    )
    ARROW_NE = Image(
        '00999:'
        '00099:'
        '00909:'
        '09000:'
        '90000:'
    )
    ARROW_E = Image(
        '00900:'
        '00090:'
        '99999:'
        '00090:'
        '00900:'
    )
    ARROW_SE = Image(
        '90000:'
        '09000:'
        '00909:'
        '00099:'
        '00999:'
    )
    ARROW_S = Image(
        '00900:'
        '00900:'
        '90909:'
        '09990:'
        '00900:'
    )
    ARROW_SW = Image(
        '00009:'
        '00090:'
        '90900:'
        '99000:'
        '99900:'
    )
    ARROW_W = Image(
        '00900:'
        '09000:'
        '99999:'
        '09000:'
        '00900:'
    )
    ARROW_NW = Image(
        '99900:'
        '99000:'
        '90900:'
        '00090:'
        '00009:'
    )
    TRIANGLE = Image(
        '00000:'
        '00900:'
        '09090:'
        '99999:'
        '00000:'
    )
    TRIANGLE_LEFT = Image(
        '90000:'
        '99000:'
        '90900:'
        '90090:'
        '99999:'
    )
    CHESSBOARD = Image(
        '09090:'
        '90909:'
        '09090:'
        '90909:'
        '09090:'
    )
    DIAMOND = Image(
        '00900:'
        '09090:'
        '90009:'
        '09090:'
        '00900:'
    )
    DIAMOND_SMALL = Image(
        '00000:'
        '00900:'
        '09090:'
        '00900:'
        '00000:'
    )
    SQUARE = Image(
        '99999:'
        '90009:'
        '90009:'
        '90009:'
        '99999:'
    )
    SQUARE_SMALL = Image(
        '00000:'
        '09990:'
        '09090:'
        '09990:'
        '00000:'
    )
    RABBIT = Image(
        '90900:'
        '90900:'
        '99990:'
        '99090:'
        '99990:'
    )
    COW = Image(
        '90009:'
        '90009:'
        '99999:'
        '09990:'
        '00900:'
    )
    MUSIC_CROTCHET = Image(
        '00900:'
        '00900:'
        '00900:'
        '99900:'
        '99900:'
    )
    MUSIC_QUAVER = Image(
        '00900:'
        '00990:'
        '00909:'
        '99900:'
        '99900:'
    )
    MUSIC_QUAVERS = Image(
        '09999:'
        '09009:'
        '09009:'
        '99099:'
        '99099:'
    )
    PITCHFORK = Image(
        '90909:'
        '90909:'
        '99999:'
        '00900:'
        '00900:'
    )
    XMAS = Image(
        '00900:'
        '09990:'
        '00900:'
        '09990:'
        '99999:'
    )
    PACMAN = Image(
        '09999:'
        '99090:'
        '99900:'
        '99990:'
        '09999:'
    )
    TARGET = Image(
        '00900:'
        '09990:'
        '99099:'
        '09990:'
        '00900:'
    )
    ALL_CLOCKS = (Image('00900:00900:00900:00000:00000:'), Image('00090:00090:00900:00000:00000:'), Image('00000:00099:00900:00000:00000:'),
                  Image('00000:00000:00999:00000:00000:'), Image('00000:00000:00900:00099:00000:'), Image('00000:00000:00900:00090:00090:'),
                  Image('00000:00000:00900:00900:00900:'), Image('00000:00000:00900:09000:09000:'), Image('00000:00000:00900:99000:00000:'),
                  Image('00000:00000:99900:00000:00000:'), Image('00000:99000:00900:00000:00000:'), Image('09000:09000:00900:00000:00000:'))
    ALL_ARROWS = (Image('00900:09990:90909:00900:00900:'), Image('00999:00099:00909:09000:90000:'), Image('00900:00090:99999:00090:00900:'),
                  Image('90000:09000:00909:00099:00999:'), Image('00900:00900:90909:09990:00900:'), Image('00009:00090:90900:99000:99900:'),
                  Image('00900:09000:99999:09000:00900:'), Image('99900:99000:90900:00090:00009:'))
    TSHIRT = Image(
        '99099:'
        '99999:'
        '09990:'
        '09990:'
        '09990:'
    )
    ROLLERSKATE = Image(
        '00099:'
        '00099:'
        '99999:'
        '99999:'
        '09090:'
    )
    DUCK = Image(
        '09900:'
        '99900:'
        '09999:'
        '09990:'
        '00000:'
    )
    HOUSE = Image(
        '00900:'
        '09990:'
        '99999:'
        '09990:'
        '09090:'
    )
    TORTOISE = Image(
        '00000:'
        '09990:'
        '99999:'
        '09090:'
        '00000:'
    )
    BUTTERFLY = Image(
        '99099:'
        '99999:'
        '00900:'
        '99999:'
        '99099:'
    )
    STICKFIGURE = Image(
        '00900:'
        '99999:'
        '00900:'
        '09090:'
        '90009:'
    )
    GHOST = Image(
        '99999:'
        '90909:'
        '99999:'
        '99999:'
        '90909:'
    )
    SWORD = Image(
        '00900:'
        '00900:'
        '00900:'
        '09990:'
        '00900:'
    )
    GIRAFFE = Image(
        '99000:'
        '09000:'
        '09000:'
        '09990:'
        '09090:'
    )
    SKULL = Image(
        '09990:'
        '90909:'
        '99999:'
        '09990:'
        '09990:'
    )
    UMBRELLA = Image(
        '09990:'
        '99999:'
        '00900:'
        '90900:'
        '09900:'
    )
    SNAKE = Image(
        '99000:'
        '99099:'
        '09090:'
        '09990:'
        '00000:'
    )


# Utils

def sleep(ms):
    return time.sleep(ms/1000)


def running_time():
    return int(time.monotonic_ns()/1000000)


# Instances

pin0 = PinFacade(adapterbit.P0)
pin1 = PinFacade(adapterbit.P1)
pin2 = PinFacade(adapterbit.P2)
pin3 = PinFacade(adapterbit.P3)
pin4 = PinFacade(adapterbit.P4)
pin5 = PinFacade(adapterbit.P5)
pin6 = PinFacade(adapterbit.P6)
pin7 = PinFacade(adapterbit.P7)
pin8 = PinFacade(adapterbit.P8)
pin9 = PinFacade(adapterbit.P9)
pin10 = PinFacade(adapterbit.P10)
pin11 = PinFacade(adapterbit.P11)
pin12 = PinFacade(adapterbit.P12)
pin13 = PinFacade(adapterbit.P13)
pin14 = PinFacade(adapterbit.P14)
pin15 = PinFacade(adapterbit.P15)
pin16 = PinFacade(adapterbit.P16)
pin19 = PinFacade(adapterbit.P19)
pin20 = PinFacade(adapterbit.P20)

i2c = I2CFacade()
display = DisplayStub()
Image = ImageImpl
