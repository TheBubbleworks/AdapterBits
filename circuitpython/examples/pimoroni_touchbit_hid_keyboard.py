import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from touchbit import *

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

keymap = [Keycode.L, Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.R]

setup()

for x in range(6):
    set_led(x, 1)
    microbit.sleep(50)
    set_led(x, 0)

while True:
    states = wait_for_change()
    if states is not None:
        for button in states:

            state = states[button]
            if state:
                key = keymap[button]
                print("Pressed {}, sending keycode {}".format(button, key))
                keyboard.press(key)
                keyboard.release_all()  # ..."Release"!
    time.sleep(0.01)