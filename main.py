from m5stack import *
from m5ui import *
from uiflow import *
import imu

score = 0
main_imu = imu.IMU()
missiles = []
bricks = []

def main(): 
    populate_bricks()
    lcd.clear(lcd.BLACK)
    draw_bricks()
    lcd.font(lcd.FONT_DejaVu18)
    update_score()
    start_time = time.time()
    game_song()

    lcd.text(lcd.CENTER, 60, "Press M5 to", lcd.GREEN)
    lcd.text(lcd.CENTER, 80, "START GAME", lcd.GREEN)

    while True:
        if btnA.wasPressed():
            break

    while len(bricks) > 0:
        x_pos = get_x_axis()
        if btnA.wasPressed():
            y_pos = 220
            shoot_missile(x_pos, y_pos)
        elif btnB.wasPressed():
            break
        update_screen(x_pos)

    end_time = time.time()
    elapsed_time = end_time - start_time 
    time_taken = "Time: {:.2f}s".format(elapsed_time)
    lcd.clear(lcd.BLACK)
    lcd.text(lcd.CENTER, 20, "Score: " + str(score), lcd.ORANGE)
    lcd.text(lcd.CENTER, 60, time_taken, lcd.YELLOW)
    lcd.text(lcd.CENTER, 100, "Final Score: " + str(score - int(elapsed_time)), lcd.GREEN)
    game_song()
    reset_game()
    main()

def update_score():
    global score
    lcd.rect(0, 0, 140, 20, color=lcd.BLACK, fillcolor=lcd.BLACK)
    lcd.text(lcd.CENTER, 0, "Score: " + str(score))

def update_screen(x_pos):
    draw_missles()
    draw_spaceship(x_pos)
    lcd.rect(0, 40, 140, 240, color=lcd.BLACK, fillcolor=lcd.BLACK)

    if(len(bricks) != 18):
        lcd.rect(0, 20, 140, 20, color=lcd.BLACK, fillcolor=lcd.BLACK)
        draw_bricks()

    wait_ms(5)

def check_missile_collision(missile):
    bricks_to_remove = []
    missiles_to_remove = []
    global score
    for brick in bricks:
        if missile[0] + 65 >= brick[0] and missile[0] + 65 <= brick[0] + 23 and missile[1] <= brick[1]:
            bricks_to_remove.append(brick)
            missiles.remove(missile)
            score += 1
            update_score()
            break

    for brick in bricks_to_remove:
        bricks.remove(brick)

def populate_bricks():
    for i in range(6):
        for j in range(3):
            new_brick = [i * 23, (j + 20) + (j * 5)]
            bricks.append(new_brick)

def shoot_missile(x_pos, y_pos):
    new_missile = [x_pos, y_pos]
    missiles.append(new_missile)

def draw_missles():
    for missile in missiles:
        lcd.circle(missile[0] + 65, missile[1], 2, 0xFFFFFF)
        missile[1] -= 6
        check_missile_collision(missile)
        if missile[1] <= 0:
            missiles.remove(missile)
            update_score()

def draw_bricks():
    for brick in bricks:
        if brick[1] < 30:
            lcd.rect(brick[0], brick[1], 22, 5, 0x00CC00)
        elif brick[1] < 40:
            lcd.rect(brick[0], brick[1], 22, 5, 0xFF0000)
         
def draw_spaceship(x_pos):
    lcd.triangle(55 + x_pos, 235, 65 + x_pos, 220, 75 + x_pos, 235, 0xFFFFFF)

def get_x_axis():
    x = int(main_imu.acceleration[0] * -100)
    if x > 70:
        x = 70
    elif x < -65:
        x = -65
    return x

def game_song():
    play_mario()

def play_note(freq, duration):
    speaker.tone(1000, 0)
    speaker.tone(freq, duration)

def play_mario():
    notes = [262, 262, 0, 262, 0, 196, 262, 0, 329, 0, 0, 0, 196, 0, 0, 0]
    durations = [200, 200, 200, 200, 200, 200, 400, 200, 400, 200, 200, 200, 400, 200, 200, 200]
    for i in range(len(notes)):
        play_note(notes[i], durations[i])

def reset_game():
    global score 
    score = 0
    global missiles
    missiles = []
    global bricks 
    bricks = []

main()
