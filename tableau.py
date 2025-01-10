import numpy as np
class Tableau:
    def __init__(self, numvars = 0, numconstraints = 0, numslack = 0, numartificial = 0, type = 'Max'):
        self.numvars = numvars
        self.numconstraints = numconstraints
        self.rows = 0
        self.tableau = np.empty((0, numvars + 1))
        self.objective = np.array([])
        self.slack = {}
        self.artificial = {}
        self.numslack = 0
        self.numartificial = 0
        self.type = type
        self.basicvars = {}
        
    def addObjective(self, obj):
        self.objective = obj
    def getTableau(self):
        return self.tableau
    def addRow(self, row):
        row.updateConstraint()
        self.tableau = np.append(self.tableau, [row.getCosntraint()], axis=0)
        if not row.getCononical():
            self.slack[self.rows] = row.getSlackValue()
            if self.slack[self.rows] == -1:
                self.numartificial += 1
                self.artificial[self.rows] = 1
            self.numslack += 1
        else:
            self.numartificial += 1
            self.artificial[self.rows] = 1
        self.rows += 1
    def addSlacks(self):
        for i in self.slack:
            slackcol = np.zeros(self.tableau.shape[0])
            slackcol[i] = self.slack[i]
            if self.slack[i] == 1:
                self.basicvars[i] = self.tableau.shape[1]-1
            self.tableau = np.insert(self.tableau, self.tableau.shape[1]-1, slackcol, axis=1)
            self.numvars += 1
    def addArtificial(self):
        for i in self.artificial:
            artcol = np.zeros(self.tableau.shape[0])
            artcol[i] = self.artificial[i]
            self.basicvars[i] = self.tableau.shape[1]-1
            self.tableau = np.insert(self.tableau, self.tableau.shape[1]-1, artcol, axis=1)
            self.numvars += 1