#!usr/bin/env python


'''

ToDo.py

by Mitchell Nordine

My CLI ToDo.

Usage:
    ToDo.py
    ToDo.py [-h | --help] [-v | --version]
    ToDo.py <project>

Options:
    -h --help           Show this screen.
    -v --version        Show version.

'''


import os, sys
import curses
import curses.textpad as textpad
from pprint import pprint

win = curses.initscr()
HEIGHT, WIDTH = win.getmaxyx()
tbox = textpad.Textbox(win, insert_mode = True)
text = "TEST"


def safeExit():
    curses.endwin()
    sys.exit(0)


def getToDoTxtFP():
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def runText():
    win.addstr(10, 5, text)


def removeCharFromText():
    global text
    text = text[:-1]


def addToText(event):
    global text
    text = text+event
    win.addstr(5, 5, event)
    win.addstr(6, 5, text)


def checkEvent(event):
    if event == ord("q"):
        safeExit()
    elif event == ord("\n"):
        runText()
        resetCursor()
    elif str(event) == "\b":
        removeCharFromText()
    else:
        addToText(chr(event))
    win.addstr(HEIGHT-2, 2, text)


def drawTitle():
    win.addstr(2, 5, "ToDo List " + str(HEIGHT) + " " + str(WIDTH), curses.A_BOLD)
    win.addstr(3, 5, "---------")


def drawRectangle():
    textpad.rectangle(win, HEIGHT-3, 1, HEIGHT-1, WIDTH-2)


def resetCursor():
    text = ""
    win.move(HEIGHT-2, 2)


def mainLoop():
    '''Run the main Program Loop. Quit with "q".'''
    drawTitle()
    drawRectangle()
    resetCursor()
    while True:
        event = win.getch()
        if event:
            win.addstr(5, 5, chr(event))
            win.addstr(6, 5, text)
            checkEvent(event)


def setupCurses():
    curses.noecho()
    #curses.curs_set(0)
    win.keypad(1)


def setup():
    setupCurses()


def main():
    fp = getToDoTxtFP()
    print(fp)
    setup()
    #try:
    mainLoop()
    #except Exception, e:
    #    pprint(e)
    #    safeExit()


if __name__ == "__main__":
    main() 


safeExit()
