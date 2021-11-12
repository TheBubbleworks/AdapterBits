import microbit

I2C_ADDR = 0x2c


def i2c_read(address, register, length=1):
    microbit.i2c.write(address, bytes([register]), repeat=True)
    return microbit.i2c.read(address, length)


def i2c_write(address, register, values):
    if type(values) is not list:
        values = [values]
    values.insert(0, register)
    microbit.i2c.write(address, bytes(values))


def set_led(index, state):
    current = i2c_read(I2C_ADDR, 0x74)[0]
    index = min(5, index)
    if state:
        current |= 1 << index
    else:
        current &= ~(1 << index)
    i2c_write(I2C_ADDR, 0x74, current)


def wait_for_change(timeout=500):
    t_start = microbit.running_time()
    while microbit.running_time() < t_start + timeout:
        if i2c_read(I2C_ADDR, 0x00)[0] & 1:             # Read status register
            button_state = i2c_read(I2C_ADDR, 0x03)[0]  # Read input states
            i2c_write(I2C_ADDR, 0x00, 0x00)             # Clear status register

            states = {}
            for x in range(6):
                states[x] = (button_state & (1 << x)) > 0

            return states
    return None


def setup():
    i2c_write(I2C_ADDR, 0x72, 0x00)  # Unlink LEDs
    i2c_write(I2C_ADDR, 0x74, 0x00)  # Clear LEDs
    i2c_write(I2C_ADDR, 0x2A, 0x00)  # Disable multi-touch blocking
    i2c_write(I2C_ADDR, 0x44, 0x40)  # Enable release interrupt
    i2c_write(I2C_ADDR, 0x1F, 0x30)  # Set sensitivity to 16x
    i2c_write(I2C_ADDR, 0x26, 0xFF)  # Force recalibration


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