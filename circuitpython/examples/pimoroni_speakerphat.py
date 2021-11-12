import board
import audiocore
import audiobusio
import digitalio
import time
from picobit import P0, P1, P2, P8

# https://freesound.org/people/ProjectsU012/sounds/341695/

PCM_CLK_PIN = P0    # Officially "continuous serial clock (SCK)". Typically written "bit clock (BCLK)".
PCM_FS_PIN = P1    # Officially "word select (WS)". Typically called "left-right clock (LRCLK)" or "frame sync (FS)".
PCM_DOUT_PIN = P2    # Officially "serial data (SD)", but can be called SDATA, SDIN, SDOUT, DACDAT, ADCDAT, etc.
AMP_ENABLE_PIN = P8

amp_enable = digitalio.DigitalInOut(AMP_ENABLE_PIN)
amp_enable.direction = digitalio.Direction.OUTPUT
amp_enable.value = True

f = open("assets/sound/coins.wav", "rb")
wav = audiocore.WaveFile(f)
i2s = audiobusio.I2SOut(PCM_CLK_PIN, PCM_FS_PIN, PCM_DOUT_PIN)

i2s.play(wav)

while i2s.playing:
    time.sleep(0.01)

