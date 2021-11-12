import board

P0 = board.GP26
#P0_PWM = board.GP6
P1 = board.GP27
P2 = board.GP28
P3 = board.GP7
P4 = board.GP8
P5 = board.GP22
P6 = board.GP9
P7 = board.GP10
P8 = board.GP11
P9 = board.GP12
P10 = board.GP13
P11 = board.GP17
P12 = board.GP14  # (SPI0 RX)
P13 = board.GP18  # (SPI0 TX)
P14 = board.GP16
P15 = board.GP19
P16 = board.GP15  # TODO: Double check this is ok?!?!? https://github.com/adafruit/circuitpython/issues/4034
P19 = board.GP21  # (I2C0)
P20 = board.GP20  # (I2C0)

LED_PIN = board.GP25

SCL = P19
SDA = P20
MISO = P14
MOSI = P15
SCK = P13

ALL_PINS = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P19, P20]
DIGITAL_IN_PINS = ALL_PINS
DIGITAL_OUT_PINS = ALL_PINS
ANALOG_IN_PINS = [P0, P1, P2]
ANALOG_OUT_PINS = []
I2C_PINS = [SDA, SCL]
SPI_PINS = [MISO, MOSI, SCK]
LED_PINS = [LED_PIN]
BUTTON_PINS = []
