#!usr/bin/env python


'''

help.py

Displays commands.

'''


from os import path
from EventChecker import EventChecker
from utils import drawMessage
import curses


class Helper():

    def __init__(self, win):
        self.win = win
        self.ec = EventChecker(win)
        self.ec.addTrigger(self.scrollDown, ord('j'))
        self.ec.addTrigger(self.scrollUp, ord('k'))
        self.ec.addTrigger(self.scrollDown, 10)
        self.ec.addTrigger(self.scrollUp, 11)
        self.scroll = 0
        self.f = self.getHelpTxt()

    def display(self):
        '''Display help text file, scrollable with 'j' and 'k'.'''
        try:
            h, w = self.win.getmaxyx()
            fl = self.f.readlines()
            self.scroll = 0
            while True:
                s = ""
                for i in range(h-4):
                    if self.scroll+i < len(fl):
                        s += fl[(self.scroll+i)%len(fl)]
                self.win.erase()
                self.win.addstr(2, 0, s)
                curses.curs_set(0) # Hide cursor
                event = self.ec.check()
                if event == 13:
                    break
        except Exception, e:
            self.win.erase()
            drawMessage(str(e)+"\n    Press ENTER.", self.win)

    def scrollDown(self):
        self.scroll += 1

    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1

    def getHelpTxt(self):
        return open(path.join(path.dirname(path.realpath(__file__)), "help.txt"), 'r')



