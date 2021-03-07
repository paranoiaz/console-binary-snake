import yaml
import os
import time
import pynput
import colorama
import random

from snake import SnakeSprite
from food import FoodSprite

config = yaml.safe_load(open("config.yml", "r"))

HEIGHT = WIDTH = config["grid_size"]
GRID = [[0 for coord_x in range(WIDTH)] for coord_y in range(HEIGHT)]
KEYSTROKES = ["w", "s", "a", "d"]
OPPOSITES = {"w": "s", "s": "w", "a": "d", "d": "a"}
RECENT = []
PRESSED = False
GAME = False

snake = SnakeSprite()
food = FoodSprite()


def clear_screen():
    # compatible with windows and linux
    if os.name == "nt":
        return os.system("cls")
    else:
        return os.system("clear")


def keyboard_event(key):
    global PRESSED
    if not PRESSED:
        # limiting to one press per cycle
        if not snake.direction:
            snake.direction = key.char
            PRESSED = True
        if key.char in KEYSTROKES:
            if (key.char != snake.direction) and (OPPOSITES[snake.direction] != key.char):
                snake.direction = key.char
                PRESSED = True


def check_border():
    global GAME
    if snake.x - 1 == -1 and snake.direction == "a":
        GAME = False
        return
    if snake.y - 1 == -1 and snake.direction == "w":
        GAME = False
        return
    if snake.x + 1 == WIDTH and snake.direction == "d":
        GAME = False
        return
    if snake.y + 1 == HEIGHT and snake.direction == "s":
        GAME = False
        return


def draw_grid():
    clear_screen()
    print(f"Highscore: {config['highscore']} - Score: {snake.length - 1}\n")

    for grid in GRID:
        _output = ""
        for _digit in grid:
            if _digit == 0:
                _output += f"{str(_digit)} "
            if _digit == 1:
                _output += f"{colorama.Fore.GREEN}{str(_digit)}{colorama.Style.RESET_ALL} "
            if _digit == 2:
                _output += f"{colorama.Fore.RED}{str(_digit - 1)}{colorama.Style.RESET_ALL} "
        print(_output)


def draw_snake():
    global GAME
    if GRID[snake.y][snake.x] == 1 and snake.direction:
        GAME = False
    if GRID[snake.y][snake.x] == 2:
        snake.length += 1
        food.eaten = False

    GRID[snake.y][snake.x] = 1
    RECENT.append((snake.x, snake.y))

    if len(RECENT) > snake.length:
        x, y = RECENT[0]
        RECENT.pop(0)
        if snake.direction:
            GRID[y][x] = 0


def draw_food():
    x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)

    if (x, y) in RECENT:
        # using recursion till it finds a valid position
        draw_food()
    else:
        food.eaten = True
        food.x = x
        food.y = y
        GRID[y][x] = 2


def main_menu():
    global GAME
    _text = "Welcome to Binary Snake, a game developed by github.com/paranoiaz"
    _output = []

    for letter in _text:
        if letter == " ":
            _output.append(letter)
        else:
            _output.append(random.randint(0, 1))

    for number in range(len(_output)):
        time.sleep(0.01)
        clear_screen()
        _output[number] = _text[number]
        for _char in _output:
            print(_char, end="")
        print("\n")

    print("Main menu\n1. Play\n2. Highscore\n3. Help\n")
    _choice = input("> ")

    if _choice.lower() in ("1", "play"):
        GAME = True
    elif _choice.lower() in ("2", "highscore"):
        clear_screen()
        print(f"Highscore:\n\n{config['highscore']}\n\nPress enter to go back.")
        input("> ")
        main_menu()
    elif _choice.lower() in ("3", "help"):
        clear_screen()
        print("Controls:\n\nUse 'w' to move up\nUse 's' to move down\nUse 'a' to move left\nUse 'd' to move right\n\nPress enter to go back.")
        input("> ")
        main_menu()
    else:
        print("Invalid input.")


if __name__ == "__main__":
    main_menu()
    listener = pynput.keyboard.Listener(on_press=keyboard_event)
    listener.start()

    while GAME:
        snake.move_position()
        draw_snake()
        if not GAME:
            # end loop before drawing a new grid
            break
        if not food.eaten:
            draw_food()
        draw_grid()
        time.sleep(config["snake_speed"] * 0.01)
        check_border()
        PRESSED = False

    if not GAME and snake.direction:
        score = snake.length - 1
        print(f"\nThanks for playing, your score is {score}.")
        if score > config["highscore"]:
            config["highscore"] = score
            with open("config.yml", "w") as _out:
                yaml.dump(config, _out, default_flow_style=False)