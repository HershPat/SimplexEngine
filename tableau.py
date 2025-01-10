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
        self.pivotcol = 0
        self.exitvar = 0

    def execute(self):
        self.addObjective()
        self.addSlacks()
        self.addArtificial()
        self.updatePivot()
        self.findExitVar()
    def makeObjective(self, obj):
        self.objective = np.append(self.objective, -obj)
    def getTableau(self):
        return self.tableau
    def getPivotCol(self):
        return self.pivotcol
    def getExitVar(self):
        return self.exitvar
    def addRow(self, row):
        row.updateConstraint() #Updates the constraint to see if it is normalized and cononical
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
    def addObjective(self):
        self.objective = np.append(self.objective, np.zeros(1)) # Add Zero for the solution for the objective function
        self.tableau = np.append(self.tableau, [self.objective], axis=0)
    def addSlacks(self):
        for i in self.slack:
            slackcol = np.zeros(self.tableau.shape[0])
            slackcol[i] = self.slack[i]
            if self.slack[i] == 1:
                self.basicvars[i] = self.tableau.shape[1]-1
            self.tableau = np.insert(self.tableau, self.tableau.shape[1]-1, slackcol, axis=1) # Insert Slack Column
            self.numvars += 1
    def addArtificial(self):
        for i in self.artificial:
            artcol = np.zeros(self.tableau.shape[0])
            artcol[i] = self.artificial[i]
            self.basicvars[i] = self.tableau.shape[1]-1
            self.tableau = np.insert(self.tableau, self.tableau.shape[1]-1, artcol, axis=1) # Insert Artificial Column
            self.tableau[self.tableau.shape[0]-1, self.tableau.shape[1]-2] = float('inf') # Big M value
            self.numvars += 1
    def updatePivot(self):
            self.pivotcol = np.argmin(self.tableau[self.tableau.shape[0]-1]) #returns the index of the pivot column
    def findExitVar(self):
        thetaratio = {}
        for row in range(self.tableau.shape[0]-1):
                if self.tableau[row, self.pivotcol] > 0:
                    thetaratio[row] = self.tableau[row, self.tableau.shape[1]-1] / self.tableau[row, self.pivotcol] #Find the theta ratio
        for i in thetaratio:
            if thetaratio[row] == min(thetaratio.values()):
                self.exitvar = row