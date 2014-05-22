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
from operator import itemgetter
import textwrap

win = curses.initscr()
HEIGHT, WIDTH = win.getmaxyx()
text = ""
parent = None
tasks = []
LI = 4
RI = 4


def sortTasks():
    '''Sort tasks by ID.'''
    global tasks
    tasks = sorted(tasks, key=itemgetter('ID'))


def wrapString(s, leftIndent=LI, rightIndent=RI):
    '''Soft warp string 's' at leftIndent and rightIndent.'''
    lines = textwrap.wrap(s, (WIDTH-rightIndent) - leftIndent)
    new = ""
    for line in lines:
        new = new+line+'\n'
        for i in range(LI):
            new = new+' '
    return new[:-1]


def confirm(msg):
    '''Ask for comfirmation.'''
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
    '''Draw msg in center of screen.'''
    win.addstr(int(HEIGHT/2)-int(msg.count('\n')/2), LI, msg)


def isNumber(s):
    '''Is string a number.'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def getJsonFP():
    return os.path.join(os.path.expanduser("~"), ".ToDo.json")


def loadTasks():
    '''Load tasks from .Todo.json file. If doesn't exist, make it.'''
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
    '''Save tasks to .ToDo.json file.'''
    sortTasks()
    f = open(getJsonFP(), 'w')
    json.dump(tasks, f)
    f.close()


def safeExit():
    curses.endwin()
    sys.exit(0)


def addItem(item):
    '''Add item to the list of tasks.'''
    item = stripSpaceFromEnds(item)
    if isNumber(item):
        return
    tasks.append({ 'task' : item, 'ID' : len(tasks), 'tags' : [] })
    saveTasks()


def removeItem(item):
    '''Remove item from the list of tasks.'''
    item = stripSpaceFromEnds(item)
    if not confirm("Are you sure you wish to remove '"+item+"'?"):
        return
    if isNumber(item):
        global tasks
        tasks[:] = [t for t in tasks if t.get('ID') != int(item)]
    elif item.lower() == "all":
        global tasks
        tasks = []
    else:
        global tasks
        tasks[:] = [t for t in tasks if t.get('task') != item]
    for i in range(len(tasks)):
        tasks[i]['ID'] = i
    saveTasks()


def replacePosWithInt(item):
    '''Replace string position indicators with associated int.'''
    item.replace('last', str(len(tasks)-1))
    item.replace('Last', str(len(tasks)-1))
    item.replace('LAST', str(len(tasks)-1))
    item.replace('end', str(len(tasks)-1))
    item.replace('End', str(len(tasks)-1))
    item.replace('END', str(len(tasks)-1))
    item.replace('first', "0")
    item.replace('First', "0")
    item.replace('FIRST', "0")
    item.replace('begin', "0")
    item.replace('Begin', "0")
    item.replace('BEGIN', "0")
    item.replace('front', "0")
    item.replace('Front', "0")
    item.replace('FRONT', "0")
    return item


def moveItem(item):
    '''Move item in first position to item in second position.'''
    item = stripSpaceFromEnds(item)
    item = replacePosWithInt(item)
    IDs = item.split(" ")
    if len(IDs) != 2:
        return
    elif not isNumber(IDs[0]) or not isNumber(IDs[1]):
        return
    IDa = int(IDs[0])
    IDb = int(IDs[1])
    if not IDa < len(tasks) and not IDa >= 0 or IDa == IDb:
        return
    if IDb >= len(tasks):
        IDb = len(tasks)-1
    elif IDb < 0:
        IDb = 0
    for t in tasks:
        if t.get('ID') == IDa:
            t['ID'] = IDb
        elif t.get('ID') >= IDb and not t.get('ID') > IDa:
            t['ID'] = t['ID']+1
    saveTasks()


def checkForExit():
    '''Check text buffer for indication to exit program.'''
    check = text.lower()
    if check == "q" or check == "x" or check == "exit" or check == "quit":
        safeExit()


def checkForAdd():
    '''Check text buffer for indication to add task.'''
    if text.lower()[:4] == "add ":
        addItem(text[4:])
    elif text.lower()[:2] == "+ ":
        addItem(text[2:])


def checkForRemove():
    '''Check text buffer for indication to remove task.'''
    if text.lower()[:3] == "rm ":
        removeItem(text[3:])
    elif text.lower()[:7] == "remove ":
        removeItem(text[7:])


def checkForMove():
    '''Check text buffer for indication to move task.'''
    if text.lower()[:3] == "mv ":
        moveItem(text[3:])
    elif text.lower()[:5] == "move ":
        moveItem(text[5:])


def stripSpaceFromEnds(s):
    '''Remove whitespace from front and back of string.'''
    while s[-1:] == " ":
        s = s[:-1]
    while s[:1] == " ":
        s = s[1:]
    return s


def executeText():
    '''Check text buffer for meaning.'''
    global text
    text = stripSpaceFromEnds(text)
    checkForExit()
    checkForAdd()
    checkForRemove()
    checkForMove()


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
    i = 0
    for task in tasks:
        t = task['task']
        ID = task['ID']
        tags = task['tags']
        s = wrapString(str(ID) + ". " + t)
        win.addstr(5 + i + 2*ID, LI, s)
        i += s.count('\n')-1


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


def setup():
    curses.noecho()
    win.keypad(1)
    global tasks
    tasks = loadTasks()


def main():
    setup()
    mainLoop()


if __name__ == "__main__":
    main() 


safeExit()
