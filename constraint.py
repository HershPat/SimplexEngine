import numpy as np
class Constraint:
    def __init__ (self, numvars = 0, inequality = '<='):
        self.constraint = np.array([])
        self.numvars = numvars
        self.inequality = inequality
        self.normalized = False
        self.isCononical = False
        self.type = ''
    def addVariable(self, var):
        self.constraint = np.append(self.constraint,var)

    def setInequality(self, inequality):
        self.inequality = inequality

    def setType(self, type):
        self.type = type

    def getCosntraint(self):
        return self.constraint
    def getCononical(self):
        return self.isCononical
    def updateConstraint(self):
        if self.type == 'Max':
            if self.inequality == '<=' or self.inequality == '=':
                self.normalized = True
                if self.inequality == '=':
                    self.isCononical = True
        elif self.type == 'Min':
            if self.inequality == '>=' or self.inequality == '=':
                self.normalized = True
                if self.inequality == '=':
                    self.isCononical = True

    # def normalize(self):
    #     if not self.normalized:
    #         if self.type == 'Max':
    #                 self.inequality = '<='
    #                 self.normalized = True
    #         elif self.type == 'Min':
    #                 self.inequality = '>='
    #                 self.normalized = True
    
    def getSlackValue(self):
        if self.type == 'Max':
            if not self.isCononical:
                if not self.normalized:
                    return -1
                else:
                    return 1
        elif self.type == 'Min':
            if not self.isCononical:
                if not self.normalized:
                    return 1
                else:
                    return -1
    