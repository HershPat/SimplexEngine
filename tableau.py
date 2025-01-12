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
        self.M = 1e6

    def execute(self):
        self.addObjective()
        self.addSlacks()
        self.addArtificial()
        if self.numartificial > 0:
            for i in self.basicvars:
                if i+self.numvars+self.numslack in self.basicvars.values():
                    self.tableau[-1] -= self.tableau[-1, self.basicvars[i]] * self.tableau[i]
        self.solve()
    def solve(self):
        if self.type == 'Max':
            while np.any(self.tableau[-1, :-1] < 0):  # Check for negative coefficients
                self.updatePivot()
                self.findExitVar()
                self.pivot()
        if self.type == 'Min':
            while np.any(self.tableau[-1, :-1] > 0):
                self.updatePivot()
                self.findExitVar()
                self.pivot()

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
            # self.numvars += 1
    def addArtificial(self):
        for i in self.artificial:
            artcol = np.zeros(self.tableau.shape[0])
            artcol[i] = self.artificial[i]
            self.basicvars[i] = self.tableau.shape[1]-1
            self.tableau = np.insert(self.tableau, self.tableau.shape[1]-1, artcol, axis=1) # Insert Artificial Column
            # self.tableau[self.tableau.shape[0]-1, self.tableau.shape[1]-2] = float('inf') # Big M value
            # self.numvars += 1
            if self.type == 'Max':
                self.tableau[-1, self.tableau.shape[1] - 2] += self.M
            elif self.type == 'Min':
                self.tableau[-1, self.tableau.shape[1] - 2] -= self.M
    def updatePivot(self):
        if self.type == 'Max':
            self.pivotcol = np.argmin(self.tableau[self.tableau.shape[0]-1, :-1]) #returns the index of the pivot column
        elif self.type == 'Min':
            self.pivotcol = np.argmax(self.tableau[self.tableau.shape[0]-1, :-1])
    def findExitVar(self):
        thetaratio = {}
        for row in range(self.tableau.shape[0]-1):
                if self.tableau[row, self.pivotcol] > 0:
                    thetaratio[row] = self.tableau[row, self.tableau.shape[1]-1] / self.tableau[row, self.pivotcol] #Find the theta ratio
        self.exitvar = min(thetaratio, key=thetaratio.get)

        
    def pivot(self):
        pivrow = self.exitvar
        pivcol = self.pivotcol
        pivval = self.tableau[pivrow, pivcol]

        self.tableau[pivrow] /= pivval #Divide the pivot row by the pivot value

        for row in range(self.tableau.shape[0]):
            if row != pivrow:
                self.tableau[row] -= self.tableau[row, pivcol] * self.tableau[pivrow] #Row operation to make other rows zero in the pivot column
        
        self.basicvars[pivrow] = pivcol
    def printSol(self):
        print("\nOptimal Solution:")
        if self.numvars+self.numslack in self.basicvars.values():
            print(f'The solution is infeasible')
            return
        rowsList = list(self.basicvars.keys())
        colList = list(self.basicvars.values())
        for i in range(self.numvars):
            if i in self.basicvars.values():
                row = rowsList[colList.index(i)]
                print(f"x{i+1} = {self.tableau[row, -1]:.3}")
            else:
                print(f"x{i+1} = 0.0")
        for i in range(self.numslack):
            slackIndex = self.numvars + i
            if slackIndex in self.basicvars.values():
                row = rowsList[colList.index(slackIndex)]
                print(f"s{i+1} = {self.tableau[row, -1]:.3}")
            else:
                    print(f"s{i+1} = 0.0")
        print(f"\nOptimal value: {self.tableau[-1, -1]:.3}")