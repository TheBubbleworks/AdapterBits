import time
import pwmio
from adapterbit import P0

# TODO: durations
# TODO: patterns and other microbit API features

# https://github.com/bbcmicrobit/micropython/blob/a92ca9b1f907c07a01116b0eb464ca4743a28bf1/docs/music.rst

# https://github.com/bbcmicrobit/micropython/blob/a92ca9b1f907c07a01116b0eb464ca4743a28bf1/source/microbit/modmusictunes.c

NOTE_FREQ_MAP = {
    'c2': 65,
    'b2': 123,
    'c3': 131,
    'a4': 440,
    'a#4': 466,
    'b4': 494,
    'c': 262,
    'c4': 262,
    'd': 294,
    'd4': 294,
    'd#4': 311,
    'd#': 311,
    'e': 330,
    'e4': 330,
    'f': 349,
    'f4': 349,
    'f#': 370,
    'f#4': 370,
    'g': 392,
    'g4': 392,
    'g#4': 415,
    'c5': 523,
}


DADADADUM = ('r4:2', 'g', 'g', 'g', 'eb:8', 'r:2', 'f', 'f', 'f', 'd:8')
ENTERTAINER = ('d4:1', 'd#', 'e', 'c5:2', 'e4:1', 'c5:2', 'e4:1', 'c5:3', 'c:1', 'd', 'd#', 'e', 'c', 'd', 'e:2', 'b4:1', 'd5:2', 'c:4')
PRELUDE = ('c4:1', 'e', 'g', 'c5', 'e', 'g4', 'c5', 'e', 'c4', 'e', 'g', 'c5', 'e', 'g4', 'c5', 'e', 'c4', 'd', 'g', 'd5', 'f', 'g4', 'd5', 'f', 'c4', 'd', 'g', 'd5', 'f', 'g4', 'd5', 'f', 'b3', 'd4', 'g', 'd5', 'f', 'g4', 'd5', 'f', 'b3', 'd4', 'g', 'd5', 'f', 'g4', 'd5', 'f', 'c4', 'e', 'g', 'c5', 'e', 'g4', 'c5', 'e', 'c4', 'e', 'g', 'c5', 'e', 'g4', 'c5', 'e')
ODE = ('e4', 'e', 'f', 'g', 'g', 'f', 'e', 'd', 'c', 'c', 'd', 'e', 'e:6', 'd:2', 'd:8', 'e:4', 'e', 'f', 'g', 'g', 'f', 'e', 'd', 'c', 'c', 'd', 'e', 'd:6', 'c:2', 'c:8')
NYAN = ('f#5:2', 'g#', 'c#:1', 'd#:2', 'b4:1', 'd5:1', 'c#', 'b4:2', 'b', 'c#5', 'd', 'd:1', 'c#', 'b4:1', 'c#5:1', 'd#', 'f#', 'g#', 'd#', 'f#', 'c#', 'd', 'b4', 'c#5', 'b4', 'd#5:2', 'f#', 'g#:1', 'd#', 'f#', 'c#', 'd#', 'b4', 'd5', 'd#', 'd', 'c#', 'b4', 'c#5', 'd:2', 'b4:1', 'c#5', 'd#', 'f#', 'c#', 'd', 'c#', 'b4', 'c#5:2', 'b4', 'c#5', 'b4', 'f#:1', 'g#', 'b:2', 'f#:1', 'g#', 'b', 'c#5', 'd#', 'b4', 'e5', 'd#', 'e', 'f#', 'b4:2', 'b', 'f#:1', 'g#', 'b', 'f#', 'e5', 'd#', 'c#', 'b4', 'f#', 'd#', 'e', 'f#', 'b:2', 'f#:1', 'g#', 'b:2', 'f#:1', 'g#', 'b', 'b', 'c#5', 'd#', 'b4', 'f#', 'g#', 'f#', 'b:2', 'b:1', 'a#', 'b', 'f#', 'g#', 'b', 'e5', 'd#', 'e', 'f#', 'b4:2', 'c#5')
RINGTONE = ('c4:1', 'd', 'e:2', 'g', 'd:1', 'e', 'f:2', 'a', 'e:1', 'f', 'g:2', 'b', 'c5:4')
FUNK = ('c2:2', 'c', 'd#', 'c:1', 'f:2', 'c:1', 'f:2', 'f#', 'g', 'c', 'c', 'g', 'c:1', 'f#:2', 'c:1', 'f#:2', 'f', 'd#')
BLUES = ('c2:2', 'e', 'g', 'a', 'a#', 'a', 'g', 'e', 'c2:2', 'e', 'g', 'a', 'a#', 'a', 'g', 'e', 'f', 'a', 'c3', 'd', 'd#', 'd', 'c', 'a2', 'c2:2', 'e', 'g', 'a', 'a#', 'a', 'g', 'e', 'g', 'b', 'd3', 'f', 'f2', 'a', 'c3', 'd#', 'c2:2', 'e', 'g', 'e', 'g', 'f', 'e', 'd')
BIRTHDAY = ('c4:3', 'c:1', 'd:4', 'c:4', 'f', 'e:8', 'c:3', 'c:1', 'd:4', 'c:4', 'g', 'f:8', 'c:3', 'c:1', 'c5:4', 'a4', 'f', 'e', 'd', 'a#:3', 'a#:1', 'a:4', 'f', 'g', 'f:8')
WEDDING = ('c4:4', 'f:3', 'f:1', 'f:8', 'c:4', 'g:3', 'e:1', 'f:8', 'c:4', 'f:3', 'a:1', 'c5:4', 'a4:3', 'f:1', 'f:4', 'e:3', 'f:1', 'g:8')
FUNERAL = ('c3:4', 'c:3', 'c:1', 'c:4', 'd#:3', 'd:1', 'd:3', 'c:1', 'c:3', 'b2:1', 'c3:4')
PUNCHLINE = ('c4:3', 'g3:1', 'f#', 'g', 'g#:3', 'g', 'r', 'b', 'c4')
PYTHON = ('d5:1', 'b4', 'r', 'b', 'b', 'a#', 'b', 'g5', 'r', 'd', 'd', 'r', 'b4', 'c5', 'r', 'c', 'c', 'r', 'd', 'e:5', 'c:1', 'a4', 'r', 'a', 'a', 'g#', 'a', 'f#5', 'r', 'e', 'e', 'r', 'c', 'b4', 'r', 'b', 'b', 'r', 'c5', 'd:5', 'd:1', 'b4', 'r', 'b', 'b', 'a#', 'b', 'b5', 'r', 'g', 'g', 'r', 'd', 'c#', 'r', 'a', 'a', 'r', 'a', 'a:5', 'g:1', 'f#:2', 'a:1', 'a', 'g#', 'a', 'e:2', 'a:1', 'a', 'g#', 'a', 'd', 'r', 'c#', 'd', 'r', 'c#', 'd:2', 'r:3')
BADDY = ('c3:3', 'r', 'd:2', 'd#', 'r', 'c', 'r', 'f#:8')
CHASE = ('a4:1', 'b', 'c5', 'b4', 'a:2', 'r', 'a:1', 'b', 'c5', 'b4', 'a:2', 'r', 'a:2', 'e5', 'd#', 'e', 'f', 'e', 'd#', 'e', 'b4:1', 'c5', 'd', 'c', 'b4:2', 'r', 'b:1', 'c5', 'd', 'c', 'b4:2', 'r', 'b:2', 'e5', 'd#', 'e', 'f', 'e', 'd#', 'e')
BA_DING = ('b5:1', 'e6:3')
WAWAWAWAA = ('e3:3', 'r:1', 'd#:3', 'r:1', 'd:4', 'r:1', 'c#:8')
JUMP_UP = ('c5:1', 'd', 'e', 'f', 'g')
JUMP_DOWN = ('g5:1', 'f', 'e', 'd', 'c')
POWER_UP = ('g4:1', 'c5', 'e', 'g:2', 'e:1', 'g:3')
POWER_DOWN = ('g5:1', 'd#', 'c', 'g4:2', 'b:1', 'c5:3')

class Music:

    BUZZER_PIN = P0

    def __init__(self):
        self.buzzer = pwmio.PWMOut(Music.BUZZER_PIN, duty_cycle=0, frequency=440, variable_frequency=True)

    def play(self, value):
        if isinstance(value, str):
            freq = self.freq_for_note(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            print("Music pattern: ", value)

            for note in value:
                print(note)
                parts = note.split(':')
                duration = 0.1
                if len(parts) > 1:
                    duration = float(parts[1])/16

                freq = self.freq_for_note(parts[0])
                self._play_freq(freq, duration)

            return
        else:
            freq = value

        self._play_freq(freq)

    def _play_freq(self, freq, duration=0.2):
        print("_play_freq", freq)
        self.buzzer.frequency = freq
        self.buzzer.duty_cycle = 65535 >> 2  # On 50%
        time.sleep(duration)
        self.buzzer.duty_cycle = 0  # Off

    def play_note(self, note):
        self.play(self.freq_for_note(note))

    @classmethod
    def freq_for_note(cls, note):
        return NOTE_FREQ_MAP[note.lower()]


_music = Music()
play = _music.play