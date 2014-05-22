#!usr/bin/env python


'''

ToDo.py

by Mitchell Nordine

My CLI ToDo.

Usage:
    ToDo.py
    ToDo.py [-h | --help] [-v | --version]
    ToDo.py <tag>

Options:
    -h --help           Show this screen.
    -v --version        Show version.

'''


import os, sys, json
import curses
import curses.textpad as textpad
from pprint import pprint

win = curses.initscr()
HEIGHT, WIDTH = win.getmaxyx()
text = ""
tasks = []


def getJsonFP():
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def loadTasks():
    try:
        f = open(getJsonFP(), 'r')
        data = json.loads(f.read())
        f.close()
        return data
    except Exception, e:
        f = open(getJsonFP(), 'w')
        json.dump([], f)
        f.close()
        return loadTasks()


def saveTasks():
    f = open(getJsonFP(), 'w')
    json.dump(tasks, f)
    f.close()


def safeExit():
    #if tasks:
    #    saveTasks()
    curses.endwin()
    sys.exit(0)


def addItemToList(item):
    item = stripSpaceFromEnds(item)
    tasks.append({ "task" : item, "ID" : len(tasks), "tags" : [] })
    saveTasks()


def checkForExit():
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()


def checkForAdd():
    if text.lower()[:4] == "add ":
        addItemToList(text[4:])
    elif text.lower()[:2] == "+ ":
        addItemToList(text[2:])


def stripSpaceFromEnds(s):
    while s[-1:] == " ":
        s = s[:-1]
    while s[:1] == " ":
        s = s[1:]
    return s


def executeText():
    global text
    text = stripSpaceFromEnds(text)
    checkForExit()
    checkForAdd()


def removeCharFromText():
    global text
    text = text[:-1]


def addToText(event):
    global text
    text = text+event


def checkEvent(event):
    if event == ord("\n"):
        executeText()
        resetCursor()
    elif event == curses.KEY_BACKSPACE or int(event) == 127:
        removeCharFromText()
    else:
        addToText(chr(event))
    #win.addstr(1, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(event), event & 255, event, event))


def drawText():
    win.addstr(HEIGHT-2, 2, text)


def drawTasks():
    for task in tasks:
        t = task['task']
        ID = task['ID']
        tags = task['tags']
        s = str(ID) + ". " + t
        win.addstr(5 + 2*ID, 4, s)


def drawTitle():
    win.addstr(2, 4, "ToDo List")
    win.addstr(3, 4, "---------")


def drawRectangle():
    textpad.rectangle(win, HEIGHT-3, 1, HEIGHT-1, WIDTH-2)


def resetCursor():
    global text
    text = ""
    win.move(HEIGHT-2, 2)


def drawAll():
    '''Draw everything.'''
    drawTitle()
    drawRectangle()
    drawTasks()
    drawText()


def mainLoop():
    '''Run the main Program Loop. Quit with "q".'''
    drawAll()
    resetCursor()
    while True:
        event = win.getch()
        if event:
            win.clear()
            checkEvent(event)
            drawAll()


def setupCurses():
    curses.noecho()
    win.keypad(1)


def setup():
    setupCurses()
    global tasks
    tasks = loadTasks()


def main():
    setup()
    mainLoop()


if __name__ == "__main__":
    main() 


safeExit()
