import time
import busio
from adapterbit import SCL, SDA, SCK, MOSI
from pianohat import PianoHat
from audio import Audio
from display import Display
from tracker import TrackerScreen
(SCREEN_WIDTH, SCREEN_HEIGHT) = (240, 240)


i2c = busio.I2C(SCL, SDA)
spi = busio.SPI(SCK, MOSI)

while not i2c.try_lock():
    pass

class MusicUtils:

    @classmethod
    def freq_for_note(cls, note):
        note_freq_map = {
            'a': 440,
            'a#': 466,
            'b': 494,
            'c': 262,
            'c#': 271,
            'd': 294,
            'd#': 311,
            'e': 330,
            'f': 349,
            'f#': 370,
            'g': 392,
            'g#': 415,

            'a4': 440,
            'a#4': 466,
            'b4': 494,
            'c4': 262,
            'c#4': 271,
            'd4': 294,
            'd#4': 311,
            'e4': 330,
            'f4': 349,
            'f#4': 370,
            'g4': 392,
            'g#4': 415,
            'c5': 523,
        }
        return note_freq_map[note.lower()]

def on_tracker_event(event_id, row, col, marker_id, note):
    print(event_id, row, col, marker_id)
    #if event_id == TrackerScreen.BEAT_MARKER_CELL:
    #freq = MusicUtils.freq_for_note(note)
    #audio.play_tone(freq)
    audio.play_sample(2,row+1)



try:
    audio = Audio()
    display = Display(spi, SCREEN_WIDTH, SCREEN_HEIGHT)
    piano_hat = PianoHat(i2c)

    tracker_screen = TrackerScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    tracker_screen.event_handler = on_tracker_event

    display.show(tracker_screen.group)

    drum_map = {
        0: "assets/audio/drums/000_base.wav",
        2: "assets/audio/drums/001_cowbell.wav",
        4: "assets/audio/drums/002_clash.wav",
        8: "assets/audio/drums/003_whistle.wav",
        10: "assets/audio/drums/004_rim.wav",
        12: "assets/audio/drums/005_hat.wav",
        13: "assets/audio/drums/006_snare.wav",
        14: "assets/audio/drums/007_clap.wav",
    }

    while True:
        now = time.monotonic_ns()

        # key_presses = piano_hat.get_keys()
        # print(key_presses)
        # for idx, is_pressed in enumerate(key_presses):
        #     if is_pressed and idx in drum_map:
        #         #audio.play_sample_file(drum_map[idx])
        #         tracker_screen.add_now(idx, TrackerScreen.BEAT_MARKER_CELL)
        notes = piano_hat.get_notes()
        for note, idx in notes.items():
            #freq = MusicUtils.freq_for_note(note)
            #audio.play_tone(freq)
            audio.play_sample(2, idx+1)
            tracker_screen.add_now(idx, TrackerScreen.BEAT_MARKER_CELL, note)

        tracker_screen.tick()
        time.sleep(0.25)
        display.refresh()

finally:
    i2c.unlock()
