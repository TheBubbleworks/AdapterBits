from touchbit import *

if __name__ == '__main__':
    setup()
    for x in range(6):
            set_led(x, 1)
            microbit.sleep(100)
            set_led(x, 0)
            microbit.sleep(100)

    while True:
        states = wait_for_change()
        if states is not None:
            for button in states:
                state = states[button]
                if button == 5:
                    microbit.display.set_pixel(0, 1, state)
                else:
                    microbit.display.set_pixel(button, 0, state)
                set_led(button, state)