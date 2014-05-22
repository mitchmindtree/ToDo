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
import textwrap

win = curses.initscr()
HEIGHT, WIDTH = win.getmaxyx()
text = ""
tasks = []
LI = 4
RI = 4


def wrapString(s, leftIndent=LI, rightIndent=RI):
    lines = textwrap.wrap(s, (WIDTH-rightIndent) - leftIndent)
    new = ""
    for line in lines:
        new = new+line+'\n'
        for i in range(LI):
            new = new+' '
    return new[:-1]


def confirm(msg):
    win.clear()
    drawRectangle()
    resetCursor()
    drawMessage(wrapString(msg + " (y/n)"))
    k = win.getch()
    win.clear()
    if chr(k).lower() == "y":
        return True
    else:
        return False


def drawMessage(msg):
    win.addstr(int(HEIGHT/2)-int(msg.count('\n')/2), LI, msg)


def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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


def addItem(item):
    item = stripSpaceFromEnds(item)
    tasks.append({ 'task' : item, 'ID' : len(tasks), 'tags' : [] })
    saveTasks()


def removeItem(item):
    item = stripSpaceFromEnds(item)
    if not confirm("Are you sure you wish to remove '"+item+"'?"):
        return
    if isNumber(item):
        global tasks
        tasks[:] = [t for t in tasks if t.get('ID') != int(item)]
    else:
        global tasks
        tasks[:] = [t for t in tasks if t.get('task') != item]
    for i in range(len(tasks)):
        tasks[i]['ID'] = i
    saveTasks()


def checkForExit():
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()


def checkForAdd():
    if text.lower()[:4] == "add ":
        addItem(text[4:])
    elif text.lower()[:2] == "+ ":
        addItem(text[2:])


def checkForRemove():
    if text.lower()[:3] == "rm ":
        removeItem(text[3:])
    elif text.lower()[:7] == "remove ":
        removeItem(text[7:])


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
    checkForRemove()


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


def drawTasks():
    '''Draws each task in the task list following it's ID.'''
    for task in tasks:
        t = task['task']
        ID = task['ID']
        tags = task['tags']
        s = wrapString(str(ID) + ". " + t)
        win.addstr(5 + 2*ID, LI, s)


def drawTitle():
    '''Draws 'ToDo List' title.'''
    win.addstr(2, LI, "ToDo List")
    win.addstr(3, LI, "---------")


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
