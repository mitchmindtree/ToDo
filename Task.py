#!usr/bin/env python


'''

Module defining the Task class for ToDo.py

'''


import os, json
from operator import itemgetter
from utils import wrapString, isNumber
from EventChecker import EventChecker
import textwrap


LI = 4
RI = 4


class Task(dict):
    '''Main Task class for ToDo.py Has keys Task, ID and Subtasks'''

    def __init__(self, win, Task=None, ID=None, Subtasks=None, Parent=None):
        self['Task'] = Task if Task is not None else "ToDo List"
        self['ID'] = ID if ID is not None else 0
        self['Subtasks'] = Subtasks if Subtasks is not None else []
        self.win = win
        self.parent = Parent if Parent is not None else self
        self.scroll = 0
        self.ec = EventChecker(win)
        self.ec.addTrigger(self.scrollDown, 10)
        self.ec.addTrigger(self.scrollUp, 11)


    def saveTasks(self, path):
        '''Save tasks to .ToDo.json file.'''
        if len(self.get('Subtasks')) > 0:
            self.sortTasks()
        else:
            self['Subtasks'] = []
        f = open(path, 'w')
        json.dump(self.get('Subtasks'), f)
        f.close()


    def loadTasks(self, path):
        '''Load tasks from .ToDo.json file to 'Subtasks'.'''
        try:
            f = open(path, 'r')
            self['Subtasks'] = json.loads(f.read())
            self.convertDictsToTasks()
            f.close()
        except Exception, e:
            self.saveTasks(path)


    def convertDictsToTasks(self):
        subtasks = []
        for d in self['Subtasks']:
            subtasks.append(Task(self.win,
                                 Task = d.get('Task'),
                                 ID = d.get('ID'),
                                 Subtasks = d.get('Subtasks'),
                                 Parent = self))
            subtasks[-1].convertDictsToTasks()
        self['Subtasks'] = subtasks


    def scrollDown(self):
        h = self.win.getmaxyx()[0]
        length = len(self.getTaskListString().split('\n'))
        if self.scroll < length and length-self.scroll > h-9:
            self.scroll += 1


    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1


    def getTaskListString(self):
        string = ""
        i = 0
        h, w = self.win.getmaxyx()
        taskIndent = ""
        for space in range(LI):
            taskIndent += " "
        subtaskIndent = ""
        for space in range(LI+7):
            subtaskIndent += " "
        for task in self.get('Subtasks'):
            t = task.get('Task')
            ID = task.get('ID')
            subtasks = task.get('Subtasks')
            s = wrapString(str(ID) + ". " + t, self.win)
            #self.win.addstr(5 + i + 2*ID, LI, s)
            i = s.count('\n')
            string += taskIndent + s
            n = 0
            for st in subtasks:
                if n < 3:
                    i += 1
                    stask = '- '+wrapString(st.get('Task'), self.win).split('\n')[0]
                    if len(stask) > w-(LI+7+4+3):
                        stask = stask[:w-(LI+7+4+3)]+"..."
                    #self.win.addstr(5 + i + 2*ID, LI+7, stask)
                    string += '\n' + subtaskIndent + stask
                    n += 1
            string += '\n\n'
        return string


    def drawTasks(self):
        '''Draws each task in 'Subtasks' following it's ID.'''
        h, w = self.win.getmaxyx()
        lines = self.getTaskListString().split('\n')
        s = ""
        for i in range(h-9):
            if self.scroll+i < len(lines):
                s += lines[(self.scroll+i)%len(lines)]+'\n'
        self.win.addstr(5, 0, s)


    def drawTitle(self):
        '''Draws 'ToDo List' title.'''
        w = self.win.getmaxyx()[1]
        s = textwrap.wrap(self.get('Task'), w-(LI+RI+3))[0]+"..."
        self.win.addstr(2, LI, s)
        underline = ""
        for i in range(len(s)):
            underline = underline+"-"
        self.win.addstr(3, LI, underline)


    def draw(self):
        self.drawTasks()
        self.drawTitle()


    def sortTasks(self):
        '''Sort subtasks by ID.'''
        self['Subtasks'] = sorted(self.get('Subtasks'), key=itemgetter('ID'))


    def addTask(self, task):
        '''Add item to the list of tasks.'''
        self['Subtasks'].append(Task(self.win, Task = task, ID = len(self['Subtasks']), Parent = self))


    def addTaskByID(self, ID, task):
        pass


    def removeTask(self, task):
        '''Remove task from subtasks.'''
        if isNumber(task):
            self['Subtasks'] = [t for t in self.get('Subtasks') if t.get('ID') != int(task)]
        elif task.lower() == "all" or task.lower() == "-a":
            self['Subtasks'] = []
        else:
            self['Subtasks'] = [t for t in self.get('Subtasks') if t.get('Task') != task]
        for i in range(len(self['Subtasks'])):
            self['Subtasks'][i]['ID'] = i


    def moveTask(self, IDa, IDb):
        '''Move task in position 'IDa' to position 'IDb'.'''
        if not IDa < len(self.get('Subtasks')) and not IDa >= 0 or IDa == IDb:
            return
        if IDb >= len(self.get('Subtasks')):
            IDb = len(self.get('Subtasks'))-1
        elif IDb < 0:
            IDb = 0
        for t in self.get('Subtasks'):
            if t.get('ID') == IDa:
                t['ID'] = IDb
            elif t.get('ID') >= IDb and not t.get('ID') > IDa:    
                t['ID'] = t['ID']+1


    def swapTasks(self, IDa, IDb):
        '''Swap task in position 'IDa' with task in position 'IDb'.'''
        if not IDa < len(self.get('Subtasks')) and not IDa >= 0 or IDa == IDb:
            return
        if not IDb < len(self.get('Subtasks')) and not IDb >= 0:
            return
        taskb = self.get('Subtasks')[IDb]
        self['Subtasks'][IDb] = self['Subtasks'][IDa]
        self['Subtasks'][IDa] = taskb


    def editTask(self, task, cbox):
        '''Edit the task name.'''
        if isNumber(task):
            if int(task) < len(self.get('Subtasks')) and int(task) >= 0:
                t = self.get('Subtasks')[int(task)]
        else:
            for item in self.get('Subtasks'):
                if item.get('Task') == task:
                    t = item
        cbox.text = t.get('Task')
        cbox.bl = 0
        cbox.br = len(cbox.text)
        while True:
            self.win.erase()
            cbox.draw()
            # EVENT CHECKER

