from tableau import Tableau
from constraint import Constraint
import numpy as np
numvars = int(input('Number of variables: '))
numconstr = int(input('Number of constraints: '))
type = (input('What type of Function (Min/Max): '))
tab = Tableau(numvars=numvars, numconstraints=numconstr, type=type)
for i in range(numconstr):
    c = Constraint(numvars = numvars)
    c.setType(type)
    for j in range(numvars):
        var = int(input(f'Enter the value for x{j+1} in constraint {i+1}: '))
        c.addVariable(var)
    inequality = input(f'Enter the inequality for constraint {i+1}: ')
    c.setInequality(inequality)
    sol = int(input(f'Enter the solution for constraint {i+1}: '))
    c.addVariable(sol)
    tab.addRow(c)
tab.addSlacks()
tab.addArtificial()
np.set_printoptions(suppress=True, precision=3)
for i in tab.getTableau():
    print(f'Constraints: {i}')