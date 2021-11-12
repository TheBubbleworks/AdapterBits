
import time


class MY_CAP1188_I2C:
    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr
        for i in range(8):
            i2c.writeto(self.addr, bytes([0x30 + i, 0x06]))
        self.i2c.writeto(self.addr, bytes([0x72, 0xff]))
        self.i2c.writeto(self.addr, bytes([0x1F, 0x60]))
        self.i2c.writeto(self.addr, bytes([0x20, 0x38]))
        self.i2c.writeto(self.addr, bytes([0x44, 0x60]))

        # Multitouch, 4 keys
        self.i2c.writeto(self.addr, bytes([0x2a, 0x04]))


    def read(self):
        self.i2c.writeto(self.addr, bytes([0,0]))
        self.i2c.writeto(self.addr,  b'\x03')
        result = bytearray(1)
        self.i2c.readfrom_into(self.addr, result)
        return result[0]


class PianoHat:

    def __init__(self, i2c):
        self.a = MY_CAP1188_I2C(i2c, 0x28)
        self.b = MY_CAP1188_I2C(i2c, 0x2b)
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']

    def read(self):
        x = self.a.read()
        y = self.b.read()

        if x > 0:
            y = 0

        data = list(reversed([x >> i & 1 for i in range(7, -1, -1)]))
        data += list(reversed([y >> i & 1 for i in range(7, -1, -1)]))
        return data


    def get_notes (self):
        touches = self.read()
        #print("touches: ", touches)
        notes = {}
        for idx, note in enumerate(self.notes):
            if touches[idx]:
                notes[note] = idx
        #print("notes: ", notes)
        return notes

    def get_keys(self):
        touches = self.read()
        return touches
