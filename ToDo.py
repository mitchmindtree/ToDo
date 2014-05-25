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
from Helper import Helper

win = curses.initscr()          # Curses Window
cbox = CommandBox(win)          # Command Box
master = Task(win)              # Master/Head Task
current = master                # Current Task Reference
helper = Helper(win)


LI = 4
RI = 4


def getJsonFP():
    '''Return path to .ToDo.json file in user directory.'''
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def safeExit():
    '''Exit safely and end the curses session.'''
    curses.endwin()
    sys.exit(0)


def checkForExit(text):
    '''Check text buffer for indication to exit program.'''
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()
    else:
        return False


def checkForHelp(text):
    '''Check text buffer for indication to display help.'''
    check = text.lower()
    if check == "h" or check == "?" or check == "help":
        helper.display()
        return True
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
    s = replacePosWithInt(s, current.get('Subtasks'))
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


def checkForSwap(text):
    '''Check text buffer for indication to swap tasks.'''
    check = text.lower()
    if check[:3] == "sw ":
        s = text[3:]
    elif check[:5] == "swap ":
        s = text[5:]
    else:
        return False
    s = stripSpaceFromEnds(s)
    s = replacePosWithInt(s, current.get('Subtasks'))
    IDs = s.split(" ")
    if len(IDs) != 2:
        return False
    elif not isNumber(IDs[0]) or not isNumber(IDs[1]):
        return False
    IDa = int(IDs[0])
    IDb = int(IDs[1])
    current.swapTasks(IDa, IDb)
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
    else:
        return False
    return True


def openTask(task):
    global current
    current = task


def closeTask():
    global current
    current = current.parent


def executeText():
    '''Check text buffer for meaning.'''
    text = stripSpaceFromEnds(cbox.text)
    if checkForExit(text): pass
    elif checkForHelp(text): pass
    elif checkForAdd(text): pass
    elif checkForRemove(text): pass
    elif checkForMove(text): pass
    elif checkForOpen(text): pass
    elif checkForClose(text): pass
    cbox.reset()
    return False


def drawHelpPrompt():
    if current == master and len(current.get('Subtasks')) == 0:
        h, w = win.getmaxyx()
        win.addstr(h-4, 2, "Type 'h', 'help' or '?' for commands.")


def drawAll():
    '''Draw everything.'''
    win.erase()
    curses.curs_set(1) # Hide cursor
    drawHelpPrompt()
    current.draw()
    cbox.draw()


def nothing():
    pass


def mainLoop():
    '''Run the main Program Loop. Quit with "q".'''
    drawAll()
    while True:
        event = cbox.check()
        current.ec.check(event)
        if event:
            drawAll()
            #win.addstr(1, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(curses.KEY_BACKSPACE), curses.KEY_BACKSPACE & 255, curses.KEY_BACKSPACE, curses.KEY_BACKSPACE))
            #win.addstr(3, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(event), event & 255, event, event))


def setTriggers():
    cbox.ec.addTrigger(executeText, 13)
    cbox.ec.addTrigger(nothing, 10) #Ctrl+j
    cbox.ec.addTrigger(nothing, 11) #Ctrl+k
    cbox.ec.addTrigger(nothing, 23) #Ctrl+w
    cbox.ec.addTrigger(nothing, 5)  #Ctrl+e
    cbox.ec.addTrigger(nothing, 18)  #Ctrl+r
    cbox.ec.addTrigger(nothing, 20)  #Ctrl+t


def setup():
    curses.noecho()
    curses.nonl()
    win.keypad(1)
    current.loadTasks(getJsonFP())
    setTriggers()


def main():
    setup()
    mainLoop()


if __name__ == "__main__":
    main() 


safeExit()

