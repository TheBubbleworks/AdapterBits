from microbit import *
import music


display.scroll("STARTED!!!")
display.scroll(i2c.scan())

# Class for driving the Kitronik :KLEF Piano
class KitronikPiano:
    CHIP_ADDRESS = 0x0D

    class PianoKeys:
        KEY_K0 = 0x100
        KEY_K1 = 0x200
        KEY_K2 = 0x400
        KEY_K3 = 0x800
        KEY_K4 = 0x1000
        KEY_K5 = 0x2000
        KEY_K6 = 0x4000
        KEY_K7 = 0x8000
        KEY_K8 = 0x01
        KEY_K9 = 0x02
        KEY_K10 = 0x04
        KEY_K11 = 0x08
        KEY_K12 = 0x10
        KEY_K13 = 0x20
        KEY_K14 = 0x40

    keySensitivity = 8
    keyNoiseThreshold = 5
    keyRegValue = 0x0000

    # Function to initialise the micro:bit Piano (called on first key press after start-up)
    def __init__(self):
        buff = bytearray(1)
        buff2 = bytearray(2)
        buff3 = bytearray(5)
        pin1.set_pull(pin1.PULL_UP)
        # Startup procedure
        # Test /change pin is low, then test basic communication

        if (pin1.read_digital() == 0):
            # Reads the chip ID, should be 0x11 (chip ID addr = 0)
            buff[0] = 0x00
            i2c.write(self.CHIP_ADDRESS, buff, False)
            reading = True
            while reading:
                readBuff = i2c.read(self.CHIP_ADDRESS, 1, False)
                if (readBuff[0] == 0x11):
                    reading = False

            # Change sensitivity (burst length) of keys 0-14 to keySensitivity (default is 8)
            for sensitivityReg in range(54, 69, 1):
                buff2[0] = sensitivityReg
                buff2[1] = self.keySensitivity
                i2c.write(self.CHIP_ADDRESS, buff2, False)

            # Disable key 15 as it is not used
            buff2[0] = 69
            buff2[1] = 0
            i2c.write(self.CHIP_ADDRESS, buff2, False)

            # Set Burst Repetition to keyNoiseThreshold (default is 5)
            buff2[0] = 13
            buff2[1] = self.keyNoiseThreshold
            i2c.write(self.CHIP_ADDRESS, buff2, False)

            # Configure Adjacent Key Suppression (AKS) Groups
            # AKS Group 1: ALL KEYS
            for aksReg in range(22, 37, 1):
                buff2[0] = aksReg
                buff2[1] = 1
                i2c.write(self.CHIP_ADDRESS, buff2, False)

            # Send calibration command
            buff2[0] = 10
            buff2[1] = 1
            i2c.write(self.CHIP_ADDRESS, buff2, False)

        # Read all change status address (General Status addr = 2)
        buff[0] = 0x02
        i2c.write(self.CHIP_ADDRESS, buff, False)
        buff3 = i2c.read(self.CHIP_ADDRESS, 5, False)
        # Continue reading change status address until /change pin goes high
        while (pin1.read_digital() == 0):
            buff[0] = 0x02
            i2c.write(self.CHIP_ADDRESS, buff, False)
            buff3 = i2c.read(self.CHIP_ADDRESS, 5, False)

    # Set sensitivity of capacitive touch keys, then initialise the IC.
    # A higher value increases the sensitivity (values can be in the range 1 - 32).
    def setKeySensitivity(self, sensitivity):
        self.keySensitivity = sensitivity
        self.__init__()

    # Set the noise threshold of capacitive touch keys, then initialise the IC.
    # A higher value enables the piano to be used in areas with more electrical noise (values can be in the range 1 - 63).
    def setKeyNoiseThreshold(self, noiseThreshold):
        self.keyNoiseThreshold = noiseThreshold
        self.__init__()

    # Function to read the Key Press Registers
    # Return value is a combination of both registers (3 and 4) which links with the values in the 'PianoKeys' class
    def _readKeyPress(self):
        buff = bytearray(1)
        buff2 = bytearray(2)
        buff3 = bytearray(5)
        buff[0] = 0x02
        i2c.write(self.CHIP_ADDRESS, buff, False)
        buff3 = i2c.read(self.CHIP_ADDRESS, 5, False)

        # Address 3 is the addr for keys 0-7 (this will then auto move onto Address 4 for keys 8-15, both reads stored in buff2)
        buff[0] = 0x03
        i2c.write(self.CHIP_ADDRESS, buff, False)
        buff2 = i2c.read(self.CHIP_ADDRESS, 2, False)

        # keyRegValue is a 4 byte number which shows which keys are pressed
        keyRegValue = (buff2[1] + (buff2[0] * 256))

        return keyRegValue

    # Function to determine if a piano key is pressed and returns a true or false output.
    def keyIsPressed(self, key: PianoKeys):
        keyPressed = False

        if (key & self._readKeyPress()) == key:
            keyPressed = True

        return keyPressed


# Test program will run forever
# Each key press will play a different note (Up and Down arrow not used)
piano = KitronikPiano()
while True:

    if piano.keyIsPressed(piano.PianoKeys.KEY_K9) is True:
        music.play('c4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K1) is True:
        music.play('c#4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K10) is True:
        music.play('d4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K2) is True:
        music.play('d#4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K11) is True:
        music.play('e4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K12) is True:
        music.play('f4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K3) is True:
        music.play('f#4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K13) is True:
        music.play('g4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K4) is True:
        music.play('g#4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K14) is True:
        music.play('a4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K5) is True:
        music.play('a#4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K6) is True:
        music.play('b4')
    if piano.keyIsPressed(piano.PianoKeys.KEY_K7) is True:
        music.play('c5')