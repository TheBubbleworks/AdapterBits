# Pimoroni Piano Hat demo
from time import sleep
from microbit import *

try:

    class cap1188:
        def __init__(self, addr):
            self.ADDRESS = addr
            for i in range(8):
                i2c.write(self.ADDRESS, bytes([0x30 + i, 0x06]), False)
            i2c.write(self.ADDRESS, bytes([0x72,0xff]),False)
            i2c.write(self.ADDRESS, bytes([0x1F,0x60]), False)
            i2c.write(self.ADDRESS, bytes([0x20,0x38]), False)
            i2c.write(self.ADDRESS, bytes([0x44,0x60]), False)

        def read(self):
            i2c.write(self.ADDRESS, bytes([0,0]), False)
            i2c.write(self.ADDRESS,  b'\x03', False)
            data = i2c.read(self.ADDRESS,1, False)
            return data[0]

    a = cap1188(0x28)
    sleep(1)
    b = cap1188(0x2b)

    class PianoHat:

        def read(self):
            x = a.read()
            y = b.read()
            if x>0:
                y = 0
            data = list(reversed([x >> i & 1 for i in range(7,-1,-1)]))
            data += list(reversed([y >> i & 1 for i in range(7,-1,-1)]))
            return data

    print("piano")
    piano_hat = PianoHat()


    class Piano:

        def __init__(self):
            # pin1 is GND
            pin1.write_digital(0)

            self.instrument = 'piano'
            self.octave = 4
            self.duration = 2

            self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        def poll(self):
            touches = piano_hat.read()

            for idx, note in enumerate(self.notes):
                if touches[idx]:
                    print(note,end='')
                    #sleep(.05)

    piano = Piano()

    while True:
        piano.poll()


except OSError as e:
    print(e)
    print("Skipping demo, PianoHAT not attached?")
    raise e