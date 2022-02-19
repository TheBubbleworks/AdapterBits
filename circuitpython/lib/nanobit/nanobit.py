import board

P0 = board.A0
P1 = board.A1
P2 = board.A2
P3 = board.A3
P4 = board.TX  # Check these!!!
P5 = board.RX
P6 = board.D2
P7 = board.D3
P8 = board.D4
P9 = board.D5
P10 = board.D6
P11 = board.D7
P12 = board.D8
P13 = board.D13
P14 = board.D12
P15 = board.D11
P16 = board.D9
P19 = board.SCL
P20 = board.SDA

LED_PIN = board.D13

SCL = P19
SDA = P20
# MISO = P14
# MOSI = P15
# SCK = P13
MISO = board.MISO
MOSI = board.MOSI
SCK = board.SCK

ALL_PINS = [P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P19, P20]
DIGITAL_IN_PINS = ALL_PINS
DIGITAL_OUT_PINS = ALL_PINS
ANALOG_IN_PINS = [P0, P1, P2, P3]
ANALOG_OUT_PINS = []
I2C_PINS = [SDA, SCL]
SPI_PINS = [MISO, MOSI, SCK]
LED_PINS = [LED_PIN]
BUTTON_PINS = []
