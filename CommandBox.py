#!usr/bin/env python


'''

Command Box for ToDo.py

'''


import curses.textpad as textpad


class CommandBox():
    '''The CommandBox class for ToDo.py'''

    def __init__(self, win):
        self.text = ""
        self.vistext = ""
        self.win = win

    def drawRect(self):
        '''Draws commandbox rectangle.'''
        h, w = self.win.getmaxyx()
        textpad.rectangle(self.win, h-3, 1, h-1, w-2)

    def drawText(self):
        '''Draw vistext within rectangel.'''
        h = self.win.getmaxyx()[0]
        self.win.addstr(h-2, 2, self.vistext)

    def draw(self):
        '''Draw all CommandBox elements.'''
        self.drawRect()
        self.drawText()

    def addChar(self, char):
        '''Add char to end of string and adjust vistext.'''
        self.text = self.text+char
        self.vistext = self.vistext+char
        if len(self.vistext) > self.getMaxVistextLen():
            self.vistext = self.vistext[1:]

    def removeChar(self):
        '''Remove char from end of string and adjust vistext.'''
        self.text = self.text[:-1]
        self.vistext = self.vistext[:-1]
        thresh = self.getRmVistextThresh()
        if len(self.vistext) <= thresh:
            self.vistext = self.text[:-thresh][-1:] + self.vistext

    def getMaxVistextLen(self):
        '''Get max drawable string length for self.vistext.'''
        w = self.win.getmaxyx()[1]
        return w - 5

    def getRmVistextThresh(self):
        '''Get string length threshold for when to scroll back vistext.'''
        return int(self.getMaxVistextLen()*2/3)
    
    def resetText(self):
        '''Resets the text buffers and moves cursor to start of textbox.'''
        h = self.win.getmaxyx()[0]
        self.text = ""
        self.vistext = ""
        self.win.move(h-2, 2)
        

