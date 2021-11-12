# Pimoroni Piano Hat demo
from bitbangio import I2C
import digitalio
import pwmio
import time

from adapterbit import P0, P1, SCL, SDA



class Music:

    BUZZER_PIN = P0


    def __init__(self):
        self.buzzer = pwmio.PWMOut(Music.BUZZER_PIN, duty_cycle=0, frequency=440, variable_frequency=True)

    def play(self, freq):
        print(freq)
        self.buzzer.frequency = freq
        self.buzzer.duty_cycle = 65535 >> 12  # On 50%
        time.sleep(0.2)
        self.buzzer.duty_cycle = 0  # Off

    def play_note(self, note):
        self.play(self.freq_for_note(note))

    @classmethod
    def freq_for_note(cls, note):
        note_freq_map = {
            'a4': 440,
            'a#4': 466,
            'b4': 494,
            'c4': 262,
            'd4': 294,
            'd#4': 311,
            'e4': 330,
            'f4': 349,
            'f#4': 370,
            'g4': 392,
            'g#4': 415,
            'c5': 523,
        }
        return note_freq_map[note]


# Class for driving the Kitronik :KLEF Piano
class KitronikPiano:
    CHIP_ADDRESS = 0x0D

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


    key_note_map = {
        KEY_K2: 'd#4',
        KEY_K3: 'f#4',
        KEY_K4: 'g#4',
        KEY_K5: 'a#4',
        KEY_K6: 'b4',
        KEY_K7: 'c5',
        KEY_K9: 'c4',
        KEY_K10: 'd4',
        KEY_K11: 'e4',
        KEY_K12: 'f4',
        KEY_K13: 'g4',
        KEY_K14: 'a4'
    }

    def all_keys(self):
        return self.key_note_map.keys()

    def note_for_key(self, key_id):
        return self.key_note_map[key_id]

    def i2c_write(self, data):
        self.i2c.writeto(self.CHIP_ADDRESS, bytes(data))

    def i2c_read(self, length):
        result = bytearray(length)
        self.i2c.readfrom_into(self.CHIP_ADDRESS, result)
        return result

    # Function to initialise the micro:bit Piano (called on first key press after start-up)
    def __init__(self):
        self.key_sensitivity = 8
        self.key_noise_threshold = 5
        self.keyRegValue = 0x0000

        self.pin1 = digitalio.DigitalInOut(P1)
        self.pin1.direction = digitalio.Direction.INPUT
        # pin1.pull = digitalio.Pull.UP

        self.i2c = I2C(SCL, SDA)

        while not self.i2c.try_lock():
            pass

        print([hex(x) for x in self.i2c.scan()])

        # Startup procedure
        # Test /change pin is low, then test basic communication
        if self.pin1.value:
            # Reads the chip ID, should be 0x11 (chip ID addr = 0)
            self.i2c_write([0])
            buff = self.i2c_read(1)
            while buff[0] != 0x11:
                buff = self.i2c_read(1)

            # Change sensitivity (burst length) of keys 0-14 to keySensitivity (default is 8)
            for sensitivity_reg in range(54, 69, 1):
                self.i2c_write([sensitivity_reg, self.key_sensitivity])

            # Disable key 15 as it is not used
            self.i2c_write([69, 0])

            # Set Burst Repetition to keyNoiseThreshold (default is 5)
            self.i2c_write([13, self.key_noise_threshold])

            # Configure Adjacent Key Suppression (AKS) Groups
            # AKS Group 1: ALL KEYS
            for aksReg in range(22, 37, 1):
                self.i2c_write([aksReg, 1])

            # Send calibration command
            self.i2c_write([10, 1])

        # Read all change status address (General Status addr = 2)
        self.i2c_write([2])
        self.i2c_read(5)
        # Continue reading change status address until /change pin goes high
        while self.pin1.value:
            self.i2c_write([2])
            self.i2c_read(5)

    # Set sensitivity of capacitive touch keys, then initialise the IC.
    # A higher value increases the sensitivity (values can be in the range 1 - 32).
    def set_key_sensitivity(self, sensitivity):
        self.key_sensitivity = sensitivity

    # Set the noise threshold of capacitive touch keys, then initialise the IC.
    # A higher value enables the piano to be used in areas with more electrical noise (values can be in the range 1 - 63).
    def set_key_noise_threshold(self, noise_threshold):
        self.key_noise_threshold = noise_threshold

    # Function to read the Key Press Registers
    # Return value is a combination of both registers (3 and 4) which links with the values in the 'PianoKeys' class
    def update(self):
        self.i2c_write([2])
        self.i2c_read(5)

        # Address 3 is the addr for keys 0-7 (this will then auto move onto Address 4 for keys 8-15, both reads stored in buff)
        self.i2c_write([3])
        buff = self.i2c_read(2)

        # keyRegValue is a 4 byte number which shows which keys are pressed
        self.keyRegValue = (buff[1] + (buff[0]*256))

    # Function to determine if a piano key is pressed and returns a true or false output.
    def key_is_pressed(self, key_id):
        return bool(key_id & self.keyRegValue)

    def notes_pressed(self):
        notes = []
        for key_id in self.all_keys():
            if self.key_is_pressed(key_id):
                notes.append(self.note_for_key(key_id))
        # print(notes)
        return notes


if __name__ == '__main__':
    music = Music()

    while True:
        for f in (262, 294, 330, 349, 392, 440, 494, 523):
            music.play(f)
            time.sleep(0.2)

    piano = KitronikPiano()

    while True:
        piano.update()
        for note_name in piano.notes_pressed():
            music.play_note(note_name)

        time.sleep(0.01)      # TODO: remove workaround for 'clock stretch'
