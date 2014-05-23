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


import os, sys, json, curses 
from pprint import pprint
from utils import *
from Task import Task
from CommandBox import CommandBox

win = curses.initscr()  # Curses Window
cbox = CommandBox(win)  # Command Box
master = Task(win)      # Master/Head Task
current = master        # Current Task Reference

LI = 4
RI = 4


def getJsonFP():
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def safeExit():
    curses.endwin()
    sys.exit(0)


def checkForExit(text):
    '''Check text buffer for indication to exit program.'''
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()
    else:
        return False


def checkForAdd(text):
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


def checkForRemove(text):
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


def checkForMove(text):
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


def checkForOpen(text):
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


def checkForClose(text):
    '''Check text buffer for indication to close task and open parent.'''
    if text.lower() == "cl":
        closeTask()
    elif text.lower() == "close":
        closeTask()
    elif text.lower() == "b":
        closeTask()
    elif text.lower() == "back":
        closeTask()


def openTask(task):
    global current
    current = task


def closeTask():
    global current
    current = current.parent


def executeText():
    '''Check text buffer for meaning.'''
    text = stripSpaceFromEnds(cbox.text)
    if checkForExit(text): return
    elif checkForAdd(text): return
    elif checkForRemove(text): return
    elif checkForMove(text): return
    elif checkForOpen(text): return
    checkForClose(text)


def checkEvent(event):
    '''Check for key event.'''
    if event == ord("\n"):
        executeText()
        cbox.resetText()
    elif event == curses.KEY_BACKSPACE or int(event) == 127:
        cbox.removeChar()
    else:
        cbox.addChar(chr(event))


def drawAll():
    '''Draw everything.'''
    current.draw()
    cbox.draw()


def mainLoop():
    '''Run the main Program Loop. Quit with "q".'''
    drawAll()
    while True:
        event = win.getch()
        if event:
            win.clear()
            try:
                checkEvent(event)
                drawAll()
            except ValueError, e:
                drawMessage(str(e)+"\n    Press ENTER.", win)
                win.addstr(1, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(event), event & 255, event, event))


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
