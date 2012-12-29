#!/usr/bin/env python

import binascii # Used for high scores
import os
import argparse
import curses
from ast import literal_eval
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_RESIZE
from random import randint

parser = argparse.ArgumentParser(description="Snake game that can be used with maps. Written using Python and ncurses.\n\nControl your snake with the arrow keys. Press 'q' to quit. Press space to pause.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-b", "--boundaries", help="Whether or not your game will end if you run into the borders.", default=False, action="store_true")
parser.add_argument("-c", "--cross", help="Allows the game to end if your snake turns directly behind itself.", default=False, action="store_true")
parser.add_argument("-d", "--dimensions", help="Dimensions in the format HEIGHTxLENGTH. If you are using a map, this value is ignored.", metavar="20x25", type=str)
parser.add_argument("-l", "--layout", help="Instead of using the arrow keys, use the layout defined in layout. Accepted layouts are wasd and vim (hjkl).", type=str, choices=['wasd','vim'])
parser.add_argument("map", help="Map file generated with rendermap.py.", nargs="?")
parser.add_argument("-n", "--number-of-food", help="How much food to put on the screen at a time.", default=1, metavar=1, type=int)
parser.add_argument("-s", "--speed", help="How fast your snake goes. Lower numbers are faster. This number is in milliseconds. Use 50 for a challenge.", default=125, metavar=125, type=int)
args = parser.parse_args()

if args.layout == "wasd":
    KEY_RIGHT = ord('d')
    KEY_LEFT = ord('a')
    KEY_UP = ord('w')
    KEY_DOWN = ord('s')
elif args.layout == "vim":
    KEY_RIGHT = ord("l")
    KEY_LEFT = ord("h")
    KEY_UP = ord("k")
    KEY_DOWN = ord("j")

key = KEY_RIGHT
score = 0
title = "SNAKE"
snake = [[4,10], [4,9], [4,8], [4,7]]
food = []

# Open our map, if guven
try:
    with open(args.map) as f:
        map_ = f.read()
        mapdict = literal_eval(map_)
        crc = binascii.crc32(map_.encode('ascii','ignore')+str(args.speed).encode('ascii','ignore')) & 0xffffffff #CRC of high score file, used to make sure that maps match for high scores. I add the speed to the end of the file so that maps at different speeds are unique.
    walls = mapdict['wall']
    use_map = True
except (IOError,TypeError) as e: # TypeError, you say? It raises one of args.map is None.
    walls = []
    use_map = False # No map found.

scr = curses.initscr()
curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

maxyx = scr.getmaxyx()
length = maxyx[1]
height = maxyx[0]

if use_map or args.dimensions:
    if use_map:
        h,l = mapdict['dimensions']
    else: #args.dimensions
        try:
            h,l = [int(a) for a in args.dimensions.split('x')]
        except:
            curses.endwin()
            raise ValueError("Your DIMENSIONS argument is improperly formatted. Please see help.")
    if h > height or l > length:
        curses.endwin()
        raise ValueError("Specified dimensions bigger than screen.")
    if h < 5 or l < 10:
        curses.endwin()
        raise ValueError("Map too small!")
    else:
        length = l+2 #compensate for border
        height = h+2

win = curses.newwin(height, length, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
#Put title in the top center
win.addstr(0, int((length/2)-(len(title)/2)), title) 

def pfood(number_of_food):
    global food
    for x in range(0,number_of_food):
        success = False
        while not success:
            food.append([randint(1, height-2), randint(1, length-2)])
            #If the food is not in the snake, the walls, or in another food
            if food[-1] in snake or food[-1] in walls or food.count(food[-1]) == 2:
                del food[-1]
            else:
                success = True

        win.addch(food[-1][0], food[-1][1], '@', curses.color_pair(3))       # Prints the food

pfood(args.number_of_food)

if use_map or food.count(food[-1]) == 2:
    for coords in walls:
        win.addch(coords[0], coords[1], ' ', curses.color_pair(2))

while True:
    win.addstr(height-1, 2, 'Score : {0}'.format(score))                # Printing 'Score'
    prevKey = key
    key = win.getch()

    if key == KEY_RESIZE or key == ord('q'):
        break

#    win.timeout(150 - (len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
    win.timeout(args.speed)

    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]:     # If an invalid key is pressed
        key = prevKey
    
    if not args.cross:
        if key == KEY_DOWN and prevKey == KEY_UP \
        or key == KEY_UP and prevKey == KEY_DOWN \
        or key == KEY_LEFT and prevKey == KEY_RIGHT \
        or key == KEY_RIGHT and prevKey == KEY_LEFT: key = prevKey

    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # Exit if snake crosses the boundaries
    if args.boundaries:
        if snake[0][0] == 0 or snake[0][0] == length-1 or snake[0][1] == 0 or snake[0][1] == height-1: break
    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = height-2
    if snake[0][1] == 0: snake[0][1] = length-2
    if snake[0][0] == height-1: snake[0][0] = 1
    if snake[0][1] == length-1: snake[0][1] = 1


    # If snake runs over itself
    if snake[0] in snake[1:]: break
    # If snake runs into a wall ;_;
    if snake[0] in walls: break
    
    if snake[0] in food:                                            # When snake eats the food
        score += 1
        food.remove(snake[0])
        pfood(1)
    else:    
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], ' ', curses.color_pair(1))

curses.endwin()

#High scores
scores = {}
filename = ".snakescores"

if not use_map:
    crc = "N{}{}{}".format(height,length,args.speed) #Yes, I know, this isn't really a "CRC". Sue me.

if not os.path.exists(filename):
    with open(filename,"w") as f:
        pass

with open(filename,"r+") as f:
    try:
        def scores_():
            try:
                scores[crc].append(score)
                scores[crc].sort()
                scores[crc].reverse()
                scores[crc] = scores[crc][:10] #Only save the highest ten scores.
            except KeyError:
                scores[crc] = [score]
        scores = literal_eval(f.read())
        scores_()
    except Exception: #Something went wrong, the file may be corrupt or non-existent.
        scores_()
    finally:
        f.seek(0)
        f.truncate()
        f.write(str(scores))

if key == KEY_RESIZE: print("Window may not be resized during gameplay. This is a feature, not a bug.")
print("Score - {}{}{}".format('\033[92m' if score > 10 else '\033[91m', score, '\033[0m'))
if score == max(scores[crc]): print("New high score!")

if use_map:
    print("Map file {} in use, CRC {}. Scores are attached to this map file and speed.".format(args.map, crc))
print("High scores for games played with window dimensions of {}x{} and a speed of {} ({}):".format(height, length, args.speed, "Hard" if args.speed <= 75 else ("Normal" if args.speed <= 125 else "Easy")))

x = 0
for score in scores[crc]:
    x += 1
    try:
        print("{}. {}".format(x,score))
    except IndexError: 
        break
