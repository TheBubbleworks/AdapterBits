import gc

print(gc.mem_free())

import time
import board
import busio
import audiobusio
import audiocore
import audiomixer

from picobit import *

PCM_CLK_PIN = P0  # Officially "continuous serial clock (SCK)". Typically written "bit clock (BCLK)".
PCM_FS_PIN = P1  # Officially "word select (WS)". Typically called "left-right clock (LRCLK)" or "frame sync (FS)".
PCM_DOUT_PIN = P2  # Officially "serial data (SD)", but can be called SDATA, SDIN, SDOUT, DACDAT, ADCDAT, etc.
AMP_ENABLE_PIN = P8

tempo = 180  # Starting BPM

# You can use the accelerometer to speed/slow down tempo by tilting!
MIN_TEMPO = 100
MAX_TEMPO = 300

SAMPLE_FOLDER = "/samples/"  # the name of the folder containing the samples
# You get 4 voices, they must all have the same sample rate and must
# all be mono or stereo (no mix-n-match!)
VOICES = [SAMPLE_FOLDER + "voice01.wav",
          SAMPLE_FOLDER + "voice02.wav"]
#          SAMPLE_FOLDER+"voice03.wav",
#          SAMPLE_FOLDER+"voice04.wav"]


audio = audiobusio.I2SOut(PCM_CLK_PIN, PCM_FS_PIN, PCM_DOUT_PIN)


def play_sample_file(filename):
    with open(filename, "rb") as f:
        wav = audiocore.WaveFile(f)
        print("%d channels, %d bits per sample, %d Hz sample rate " %
              (wav.channel_count, wav.bits_per_sample, wav.sample_rate))
        audio.play(wav)
        while audio.playing:
            time.sleep(0.01)
        print(gc.mem_free())


try:

    for filename in VOICES:
        print(filename)
        # play_sample_file (filename)
    # raise Exception("done")

    # Parse the first file to figure out what format its in
    with open(VOICES[0], "rb") as f:
        wav = audiocore.WaveFile(f)
        print("%d ch, %d bpsamp, %d Hz  " %
              (wav.channel_count, wav.bits_per_sample, wav.sample_rate))

    samples = []
    # Read the 4 wave files, convert to stereo samples, and store
    # (show load status on neopixels and play audio once loaded too!)

    for v in range(len(VOICES)):
        print("Open", VOICES[v])
        with open(VOICES[v], "rb") as wave_file:
            sample = audiocore.WaveFile(wave_file, bytearray(8 * 8192))
            samples.append(sample)
            print(gc.mem_free())

    print(samples)

    mixer = audiomixer.Mixer(voice_count=4,
                             sample_rate=wav.sample_rate,
                             channel_count=wav.channel_count,
                             bits_per_sample=wav.bits_per_sample,
                             samples_signed=True)
    audio.play(mixer)

    # Our global state
    current_step = 7  # we actually start on the last step since we increment first
    # the state of the sequencer
    beatset = [[False] * 8, [False] * 8, [False] * 8, [False] * 8]
    # currently pressed buttons
    current_press = set()

    # mixer.play(≈, voice=0)
    # mixer.play(samples[1], voice=1)

    mixer.voice[0].play(samples[0])
    mixer.voice[1].play(samples[1])

    while mixer.playing:
        print(".", end='')
        time.sleep(1)

    print("Start tracker!")
    print(gc.mem_free())

    while True:
        stamp = time.monotonic()
        # next beat!
        current_step = (current_step + 1) % 8

        # draw the vertical ticker bar, with selected voices highlighted
        for y in range(4):
            if beatset[y][current_step]:
                print("Playing: ", VOICES[y])
                mixer.play(samples[y], voice=y)

        # handle button presses while we're waiting for the next tempo beat
        # also check the accelerometer if we're using it, to adjust tempo
        while time.monotonic() - stamp < 60 / tempo:
            # Check for pressed buttons
            pressed = set()
            # print(pressed)
            for down in pressed - current_press:
                # print("Pressed down", down)
                y = down[0]
                x = down[1]
                beatset[y][x] = not beatset[y][x]  # enable the voice

            current_press = pressed

            time.sleep(0.01)  # a little delay here helps avoid debounce annoyances
finally:
    print("\nCleaning up");
    audio.stop()
    audio.deinit()

