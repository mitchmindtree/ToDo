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


import os, sys, json, curses, textwrap
import curses.textpad as textpad
from pprint import pprint
from utils import wrapString, confirm, isNumber, replacePosWithInt, stripSpaceFromEnds
from Task import Task

win = curses.initscr()
HEIGHT, WIDTH = win.getmaxyx()
text = ""
master = Task()
current = master
LI = 4
RI = 4


def getJsonFP():
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def safeExit():
    curses.endwin()
    sys.exit(0)


def checkForExit():
    '''Check text buffer for indication to exit program.'''
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()
    else:
        return False


def checkForAdd():
    '''Check text buffer for indication to add task.'''
    if text.lower()[:4] == "add ":
        s = text[4:]
    elif text.lower()[:2] == "+ ":
        s = text[2:]
    else:
        return False
    s = stripSpaceFromEnds(s)
    if isNumber(s):
        return False
    current.addTask(s)
    master.saveTasks(getJsonFP())
    return True


def checkForRemove():
    '''Check text buffer for indication to remove task.'''
    if text.lower()[:3] == "rm ":
        s = text[3:]
    elif text.lower()[:7] == "remove ":
        s = text[7:]
    else:
        return False
    s = stripSpaceFromEnds(s)
    if not confirm("Are you sure you wish to remove '"+s+"'?", win):
        return False
    current.removeTask(s)
    master.saveTasks(getJsonFP())
    return True


def checkForMove():
    '''Check text buffer for indication to move task.'''
    if text.lower()[:3] == "mv ":
        s = text[3:]
    elif text.lower()[:5] == "move ":
        s = text[5:]
    else:
        return False
    s = stripSpaceFromEnds(s)
    s = replacePosWithInt(s)
    IDs = s.split(" ")
    if len(IDs) != 2:
        return False
    elif not isNumber(IDs[0]) or not isNumber(IDs[1]):
        return False
    IDa = int(IDs[0])
    IDb = int(IDs[1])
    current.moveTask(IDa, IDb)
    master.saveTasks(getJsonFP())
    return True


def checkForOpen():
    '''Check text buffer for indication to open a Subtask as main task.'''
    if text.lower()[:2] == "o ":
        s = text[2:]
    elif text.lower()[:5] == "open ":
        s = text[5:]
    else:
        return False
    s = stripSpaceFromEnds(s)
    if isNumber(s) and int(s) >= 0 and int(s) < len(current.get('Subtasks')):
        openTask(current.get('Subtasks')[int(s)])
    else:
        for t in current.get('Subtasks'):
            if t.get('Task') == s:
                openTask(t)
    return True


def openTask(task):
    global current
    current = task


def checkForClose():
    '''Check text buffer for indication to close task and open parent.'''
    if text.lower() == "cl":
        closeTask()
    elif text.lower() == "close":
        closeTask()
    elif text.lower() == "b":
        closeTask()
    elif text.lower() == "back":
        closeTask()


def closeTask():
    global current
    current = current.parent


def executeText():
    '''Check text buffer for meaning.'''
    global text
    text = stripSpaceFromEnds(text)
    if checkForExit(): return
    elif checkForAdd(): return
    elif checkForRemove(): return
    elif checkForMove(): return
    elif checkForOpen(): return
    checkForClose()


def removeCharFromText():
    '''Remove last character from 'text' buffer.'''
    global text
    text = text[:-1]


def addToText(event):
    '''Add character to 'text' buffer.'''
    global text
    text = text+event


def checkEvent(event):
    '''Check for key event.'''
    if event == ord("\n"):
        executeText()
        resetCursor()
    elif event == curses.KEY_BACKSPACE or int(event) == 127:
        removeCharFromText()
    else:
        addToText(chr(event))
    #win.addstr(1, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(event), event & 255, event, event))


def drawText():
    '''Draw the 'text' buffer to the textbox.'''
    win.addstr(HEIGHT-2, 2, text)


def drawTitle():
    '''Draws 'ToDo List' title.'''
    s = textwrap.wrap(current.get('Task'), WIDTH-(LI+RI+3))[0]+"..."
    win.addstr(2, LI, s)
    underline = ""
    for i in range(len(s)):
        underline = underline+"-"
    win.addstr(3, LI, underline)


def drawRectangle():
    '''Draws textbox rectangle.'''
    textpad.rectangle(win, HEIGHT-3, 1, HEIGHT-1, WIDTH-2)


def resetCursor():
    '''Resets the 'text' buffer and moves cursor to start of textbox.'''
    global text
    text = ""
    win.move(HEIGHT-2, 2)


def drawAll():
    '''Draw everything.'''
    drawTitle()
    drawRectangle()
    current.drawTasks(win)
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


def setup():
    curses.noecho()
    win.keypad(1)
    current.loadTasks(getJsonFP())


def main():
    setup()
    mainLoop()


if __name__ == "__main__":
    main() 


safeExit()
