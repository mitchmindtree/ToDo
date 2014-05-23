#!usr/bin/env python


'''

Command Box for ToDo.py

'''


import curses.textpad as textpad


class CommandBox():
    '''The CommandBox class for ToDo.py'''

    def __init__(self, win):
        self.text = ""
        self.bl = 0
        self.br = 0
        self.win = win

    def drawRect(self):
        '''Draws commandbox rectangle.'''
        h, w = self.win.getmaxyx()
        textpad.rectangle(self.win, h-3, 1, h-1, w-2)

    def drawText(self):
        '''Draw vistext within rectangel.'''
        h = self.win.getmaxyx()[0]
        self.win.addstr(h-2, 2, self.getVistext())

    def draw(self):
        '''Draw all CommandBox elements.'''
        self.drawRect()
        self.drawText()

    def addChar(self, char):
        '''Add char to end of string and adjust vistext.'''
        self.text = self.text+char
        self.br += 1
        if self.br - self.bl > self.getMaxVistextLen():
            self.bl += 1

    def removeChar(self):
        '''Remove char from end of string and adjust vistext.'''
        self.text = self.text[:-1]
        thresh = self.getRmVistextThresh()
        self.br -= 1
        if self.br - self.bl <= thresh and len(self.text) > thresh:
            self.bl -= 1

    def getMaxVistextLen(self):
        '''Get max drawable string length for self.vistext.'''
        w = self.win.getmaxyx()[1]
        return w - 5

    def getRmVistextThresh(self):
        '''Get string length threshold for when to scroll back vistext.'''
        return int(self.getMaxVistextLen()*2/3)

    def getVistext(self):
        return self.text[self.bl:][:self.br]

    def shuffleVistext(self, n):
        if n < 0 and self.bl+n >= 0 and self.br+n >= self.getMaxVistextLen():
            self.bl += n
            self.br += n
        elif n > 0 and self.bl+n <= self.text-self.getMaxVistextLen() and self.br+n <= len(self.text):
            self.bl += n
            self.br += n

    def reset(self):
        resetText()
        resetCursor()
    
    def resetText(self):
        '''Resets the text buffers and moves cursor to start of textbox.'''
        h = self.win.getmaxyx()[0]
        self.text = ""
        self.bl = 0
        self.br = 0

    def resetCursor(self):
        self.win.move(h-2, 2)
        
