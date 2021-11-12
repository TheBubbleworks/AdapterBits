import board
import busio
import digitalio


led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

TX_PIN = board.GP0
RX_PIN = board.GP1

uart = busio.UART(TX_PIN, RX_PIN,  baudrate=115200)

print("Hello world!")

uart.write(b"Hello world!\r\n")

while True:
    data = uart.read(1)  # read up to 32 bytes
    # if data is None:
    #     continue
    #print(data)  # this is a bytearray type

    if data is not None:
        led.value = True

        uart.write(data)
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")

        led.value = False