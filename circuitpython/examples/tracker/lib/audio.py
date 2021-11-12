import math
import time
import array
import audiocore
import audiobusio
import audiomixer

import digitalio
from adapterbit import P0, P1, P2, P8

# https://freesound.org/people/ProjectsU012/sounds/341695/

PCM_CLK_PIN = P0    # Officially "continuous serial clock (SCK)". Typically written "bit clock (BCLK)".
PCM_FS_PIN = P1    # Officially "word select (WS)". Typically called "left-right clock (LRCLK)" or "frame sync (FS)".
PCM_DOUT_PIN = P2    # Officially "serial data (SD)", but can be called SDATA, SDIN, SDOUT, DACDAT, ADCDAT, etc.
AMP_ENABLE_PIN = P8

class Audio:

    def __init__(self):
        amp_enable = digitalio.DigitalInOut(AMP_ENABLE_PIN)
        amp_enable.direction = digitalio.Direction.OUTPUT
        amp_enable.value = True
        self.i2s = audiobusio.I2SOut(PCM_CLK_PIN, PCM_FS_PIN, PCM_DOUT_PIN)
        self.samples={}
        self.next_voice = 0
        self.max_voices = 4

        self.sample_banks = {
            1: {
                1: audiocore.WaveFile(open("/assets/audio/drums/clap.wav", "rb")),
                2: audiocore.WaveFile(open("/assets/audio/drums/whistle.wav", "rb")),
                # 3: audiocore.WaveFile(open("/assets/audio/drums/base.wav", "rb")),
                # 4: audiocore.WaveFile(open("/assets/audio/drums/clash.wav", "rb")),
                # 5: audiocore.WaveFile(open("/assets/audio/drums/cowbell.wav", "rb")),
                # 6: audiocore.WaveFile(open("/assets/audio/drums/hat.wav", "rb")),
                # 7: audiocore.WaveFile(open("/assets/audio/drums/rim.wav", "rb")),
                # 8: audiocore.WaveFile(open("/assets/audio/drums/snare.wav", "rb"))
            },
            2: {
                1: audiocore.WaveFile(open("/assets/audio/piano/1.wav", "rb")),
                2: audiocore.WaveFile(open("/assets/audio/piano/2.wav", "rb")),
                3: audiocore.WaveFile(open("/assets/audio/piano/3.wav", "rb")),
                4: audiocore.WaveFile(open("/assets/audio/piano/4.wav", "rb")),
                5: audiocore.WaveFile(open("/assets/audio/piano/5.wav", "rb")),
                6: audiocore.WaveFile(open("/assets/audio/piano/6.wav", "rb")),
                7: audiocore.WaveFile(open("/assets/audio/piano/7.wav", "rb")),
                8: audiocore.WaveFile(open("/assets/audio/piano/8.wav", "rb")),
                9: audiocore.WaveFile(open("/assets/audio/piano/9.wav", "rb")),
                10: audiocore.WaveFile(open("/assets/audio/piano/10.wav", "rb")),
                11: audiocore.WaveFile(open("/assets/audio/piano/11.wav", "rb")),
                12: audiocore.WaveFile(open("/assets/audio/piano/12.wav", "rb")),
                13: audiocore.WaveFile(open("/assets/audio/piano/13.wav", "rb"))
            }
        }

        print(self.sample_banks)
        #self.clap = audiocore.WaveFile(open("/assets/audio/drums/clap.wav", "rb"))
        #hat = audiocore.WaveFile(open("/assets/audio/drums/hat.wav", "rb"))
        #whistle = audiocore.WaveFile(open("/assets/audio/drums/whistle.wav", "rb"))
        #self.i2s.play(clap)
        #self.i2s.play(whistle)

        self.mixer = audiomixer.Mixer(voice_count=self.max_voices,
                                      sample_rate=11025,
                                      channel_count=1, bits_per_sample=16,
                                      samples_signed=True)


        # whistle = self.sample_banks[1][2]
        # clap = self.sample_banks[1][1]
        # piano1 = self.sample_banks[2][1]
        # piano2 = self.sample_banks[2][2]

        self.i2s.play(self.mixer)
        #self.mixer.voice[0].play(whistle)
        # end_time = time.monotonic() + 5000
        #
        # #while self.mixer.playing:
        # while time.monotonic() < end_time:
        #     self.mixer.voice[1].play(clap)
        #     time.sleep(0.5)
        #     self.mixer.voice[2].play(piano1)
        #     time.sleep(0.5)

        # for i in range(1, 3):
        #     print("Playing sample", i)
        #     self.mixer.voice[0].play(self.sample_banks[1][i])
        #     time.sleep(1)

        #self.mixer.voice[0].level = 0.50   # MixerVoice
        for i in range(1, 6):
            print("Playing sample", i)
            self.mixer.stop_voice(0)
            self.mixer.voice[0].play(self.sample_banks[2][i])
            time.sleep(1)
            self.mixer.stop_voice(1)
            self.mixer.voice[1].play(self.sample_banks[2][i])
            time.sleep(1)

    # def play_sample_file(self, filename):
    #     with open(filename, "rb") as f:
    #         wav = audiocore.WaveFile(f)
    #         self.i2s.play(wav)
    #         while self.i2s.playing:
    #             time.sleep(0.01)
    #
    #
    # def play_tone(self, freq=440, duration=0.1):
    #     length = 8000 // freq
    #     sine_wave = array.array("H", [0] * length)
    #
    #     if freq in self.samples:
    #         sine_wave = self.samples[freq]
    #     else:
    #         for i in range(length):
    #             sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)
    #
    #         sine_wave = audiocore.RawSample(sine_wave, sample_rate=8000)
    #         self.samples[freq] = sine_wave
    #
    #     self.i2s.play(sine_wave, loop=True)
    #     time.sleep(duration)
    #     self.i2s.stop()

    def play_sample(self, bank, sample):
        try:
            self.mixer.stop_voice(self.next_voice)
            self.mixer.voice[self.next_voice].play(self.sample_banks[bank][sample])
            self.next_voice = (self.next_voice + 1) % self.max_voices
        except KeyError:
            print("Bank[{}]Sample[{}] does not exist!".format(bank, sample))

