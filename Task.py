#!usr/bin/env python


'''

Module defining the Task class for ToDo.py

'''


import os, json
from operator import itemgetter
from utils import wrapString


class Task(dict):
    '''Main Task class for ToDo.py Has keys Task, ID and Subtasks'''

    def __init__(self, Task=None, ID=None, Subtasks=None):
        self['Task'] = Task if Task is not None else "ToDo List"
        self['ID'] = ID if ID is not None else 0
        self['Subtasks'] = Subtasks if Subtasks is not None else []


    def saveTasks(self, path):
        '''Save tasks to .ToDo.json file.'''
        if len(self.get('Subtasks')) > 0:
            sortTasks()
        else:
            self['Subtasks'] = []
        f = open(getJsonFP(), 'w')
        json.dump(self.get('Subtasks'), f)
        f.close()


    def loadTasks(self, path):
        '''Load tasks from .ToDo.json file to 'Subtasks'.'''
        try:
            f = open(path, 'r')
            self['Subtasks'] = json.loads(f.read())
            f.close()
        except Exception, e:
            saveTasks(self, path)
    

    def drawTasks(self, win):
        '''Draws each task in 'Subtasks' following it's ID.'''
        i = 0
        for task in self['Subtasks']:
            t = task.get('task')
            ID = task.get('ID')
            subtasks = task.get('Subtasks')
            s = wrapString(str(ID) + ". " + t)
            win.addstr(5 + i + 2*ID, LI, s)
            i += s.count('\n')-1


    def sortTasks(self):
        '''Sort subtasks by ID.'''
        self['Subtasks'] = sorted(self.get('Subtasks'), key=itemgetter('ID'))


    def addTask(self, task):
        '''Add item to the list of tasks.'''
        self['Subtasks'].append(Task(Task = task, ID = len(self['Subtasks'])))


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

