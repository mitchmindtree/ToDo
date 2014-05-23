#!usr/bin/env python


'''

Utility functions for ToDo.py

'''


import textwrap


LI = 4
RI = 4


def wrapString(s, win, leftIndent=LI, rightIndent=RI):
    '''Soft warp string 's' at leftIndent and rightIndent.'''
    WIDTH = win.getmaxyx()[1]
    lines = textwrap.wrap(s, (WIDTH-rightIndent) - leftIndent)
    new = ""
    for line in lines:
        new = new+line+'\n'
        for i in range(LI):
            new = new+' '
    return new[:-1]


def confirm(msg, win):
    '''Ask for comfirmation.'''
    win.clear()
    #drawRectangle()
    #resetCursor()
    drawMessage(wrapString(msg + " (y/n)", win), win)
    k = win.getch()
    win.clear()
    if chr(k).lower() == "y":
        return True
    else:
        return False


def drawMessage(msg, win):
    '''Draw msg in center of screen.'''
    h = win.getmaxyx()[0]
    win.addstr(int(h/2)-int(msg.count('\n')/2), LI, msg)



def isNumber(s):
    '''Is string a number.'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def replacePosWithInt(s, tasks):
    '''Replace string position indicators with associated int.'''
    s.replace('last', str(len(tasks)-1))
    s.replace('Last', str(len(tasks)-1))
    s.replace('LAST', str(len(tasks)-1))
    s.replace('end', str(len(tasks)-1))
    s.replace('End', str(len(tasks)-1))
    s.replace('END', str(len(tasks)-1))
    s.replace('first', "0")
    s.replace('First', "0")
    s.replace('FIRST', "0")
    s.replace('begin', "0")
    s.replace('Begin', "0")
    s.replace('BEGIN', "0")
    s.replace('front', "0")
    s.replace('Front', "0")
    s.replace('FRONT', "0")
    return s


def stripSpaceFromEnds(s):
    '''Remove whitespace from front and back of string.'''
    while s[-1:] == " ":
        s = s[:-1]
    while s[:1] == " ":
        s = s[1:]
    return s


