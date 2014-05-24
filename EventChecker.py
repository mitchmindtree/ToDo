#!usr/bin/env python


'''

A Curses Event Checker for ToDo.py

'''


import curses


class EventChecker():

    def __init__(self, win):
        self.win = win
        self.trigs = {}

    def addTrigger(self, func, event):
        if not self.trigs.has_key(event):
            self.trigs[event] = func

    def check(self, event=None):
        event = event if event is not None else self.win.getch()
        try:
            if event == curses.KEY_RESIZE:
                return event
            elif event == curses.KEY_LEFT:
                return None
            elif event == curses.KEY_RIGHT:
                return None
            elif event == curses.KEY_UP:
                return None
            elif event == curses.KEY_DOWN:
                return None
            elif self.trigs.get(event):
                self.trigs.get(event)()
            elif self.trigs.get(int(event)):
                self.trigs.get(int(event))()
            elif self.trigs.get(str(event)):
                self.trigs.get(str(event))()
            elif self.trigs.get(chr(event)):
                self.trigs.get(chr(event))()
            elif self.trigs.get('rest'):
                self.trigs.get('rest')(event)
            return event
        except ValueError, e:
            drawMessage(str(e)+"\n    Press Enter.", self.win)
            self.win.addstr(1, 4, 'key: \'%s\' <=> %c <=> 0x%X <=> %d' % (curses.keyname(event), event & 255, event, event))

