from microbit import *
import neopixel
from random import randint


# Enable NeoPixels to use x & y values
def np_plot(x, y, r, g, b):
    np[x + (y * 8)] = (r, g, b)


def start_sequence(x_position):
    if x_position == 7:
        ball_x = 1
        ball_y = 3
        direction = 1
    elif x_position == 0:
        ball_x = 6
        ball_y = 4
        direction = 2
    start_square_x = [3, 4, 3, 4]
    start_square_y = [3, 3, 4, 4]
    for start_y in start_square_y:
        for start_x in start_square_x:
            np_plot(start_x, start_y, 20, 0, 0)
    np.show()
    sleep(500)
    for start_y in start_square_y:
        for start_x in start_square_x:
            np_plot(start_x, start_y, 20, 20, 0)
    np.show()
    sleep(500)
    for start_y in start_square_y:
        for start_x in start_square_x:
            np_plot(start_x, start_y, 0, 20, 0)
    np.show()
    sleep(500)
    for start_y in start_square_y:
        for start_x in start_square_x:
            np_plot(start_x, start_y, 0, 0, 0)
    np.show()
    pin2.write_analog(511)
    pin2.set_analog_period(1)
    sleep(500)
    pin2.write_analog(0)


# Haptic feedback function
def hit():
    pin1.write_digital(1)
    sleep(150)
    pin1.write_digital(0)


# Game setup
np = neopixel.NeoPixel(pin0, 64)  # changed from 32 to 64 to get full 8x8 array
col_combo = [[0, 0, 0], [20, 0, 0], [0, 20, 0], [0, 0, 20], [20, 20, 20]]
player_1_x, player_1_y = 0, 1
player_2_x, player_2_y = 7, 6
ball_x, ball_y = 1, 3
timer, angle_up, angle_down = 0, 0, 0
direction = 1
win_count, player_1_score, player_2_score = 0, 0, 0
playing = True
end = False

display.scroll("BIT PONG")

start_sequence(7)

while playing == True:
    time.sleep(0.05)
    # Display
    # Display grid
    for y in range(0, 8):
        for x in range(0, 8):  # Changed 4 to 8 to enable 8x8 grid
            np_plot(x, y, col_combo[0][0], col_combo[0][1], col_combo[0][2])
    # Display player bars
    # Player 1
    player_1_y_bar = [player_1_y - 1, player_1_y, player_1_y + 1]
    for y_1 in player_1_y_bar:
        np_plot(player_1_x, y_1, 20, 0, 0)
    # Player 2
    player_2_y_bar = [player_2_y - 1, player_2_y, player_2_y + 1]
    for y_2 in player_2_y_bar:
        np_plot(player_2_x, y_2, 0, 0, 20)
    # Display ball
    np_plot(ball_x, ball_y, 20, 20, 20)
    np.show()

    # Movement
    # Player 1 (Red)
    # Left
    if pin8.read_digital() == 0 and player_1_y > 1:
        player_1_y -= 1
    # Right
    if pin14.read_digital() == 0 and player_1_y < 6:
        player_1_y += 1
    # Player 2 (Blue)
    # Left
    if pin16.read_digital() == 0 and player_2_y < 6:
        player_2_y += 1
    # Right
    if pin15.read_digital() == 0 and player_2_y > 1:
        player_2_y -= 1

    # Ball bounces off player 1 pad
    if direction % 2 == 0 and ball_x == 1 and (ball_y == player_1_y or ball_y == player_1_y - 1 or ball_y == player_1_y + 1):
        hit()
        direction += 1
        timer = 0
        if angle_up == 0 and angle_down == 0:
            if ball_y == player_1_y:
                angle_up = 0
                angle_down = 0
            elif ball_y == player_1_y - 1:
                angle_up = 1
                angle_down = 0
            elif ball_y == player_1_y + 1:
                angle_up = 0
                angle_down = 1
        if ball_y == 0:
            angle_up = 0
            angle_down = 1
        elif ball_y == 7:
            angle_up = 1
            angle_down = 0
    # Ball bounces off player 2 pad
    elif direction % 2 != 0 and ball_x == 6 and (ball_y == player_2_y or ball_y == player_2_y - 1 or ball_y == player_2_y + 1):
        hit()
        direction += 1
        timer = 0
        if angle_up == 0 and angle_down == 0:
            if ball_y == player_2_y:
                angle_up = 0
                angle_down = 0
            if ball_y == player_2_y - 1:
                angle_up = 1
                angle_down = 0
            elif ball_y == player_2_y + 1:
                angle_up = 0
                angle_down = 1
        if ball_y == 0:
            angle_up = 0
            angle_down = 1
        elif ball_y == 7:
            angle_up = 1
            angle_down = 0
    # Ball bounces off wall
    if ball_x > 1 and ball_x < 6:
        if ball_y == 0:
            if angle_up == 1:
                angle_up = 0
                angle_down = 1
            elif angle_down == 1:
                angle_up = 1
                angle_down = 0
        elif ball_y == 7:
            if angle_up == 1:
                angle_up = 0
                angle_down = 1
            elif angle_down == 1:
                angle_up = 1
                angle_down = 0

    # Ball movement
    timer += 1
    if timer == 3:
        if direction % 2 != 0 and angle_up == 0 and angle_down == 0:  # Straight right
            ball_x += 1
        elif direction % 2 != 0 and angle_up == 1 and angle_down == 0:  # Up from left
            ball_y -= 1
            ball_x += 1
        elif direction % 2 != 0 and angle_up == 0 and angle_down == 1:  # Down from left
            ball_y += 1
            ball_x += 1
        elif direction % 2 == 0 and angle_up == 0 and angle_down == 0:  # Straight left
            ball_x -= 1
        elif direction % 2 == 0 and angle_up == 1 and angle_down == 0:  # Up from right
            ball_y -= 1
            ball_x -= 1
        elif direction % 2 == 0 and angle_up == 0 and angle_down == 1:  # Down from right
            ball_y += 1
            ball_x -= 1
        timer = 0

    # Scoring
    if ball_x == 0 or ball_x == 7:
        np.clear()
        win_count += 1
        if ball_x == 7:
            player_1_score += 1
            ball_x = 1
            ball_y = 3
            direction = 1
        if ball_x == 0:
            player_2_score += 1
            ball_x = 6
            ball_y = 4
            direction = 2
        if win_count < 3:
            start_sequence(ball_x)

    # Game end check
    if win_count >= 3:
        playing = False
        end = True

if end == True:
    np.clear()
    if player_1_score > player_2_score:
        display.scroll('Red Wins!', wait=False, loop=True)
    elif player_2_score > player_1_score:
        display.scroll('Blue Wins!', wait=False, loop=True)