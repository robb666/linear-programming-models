
from pulp import *
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

model = LpProblem(name='insurance_profit', sense=LpMaximize)

# Definition of decision variables
x = {i: LpVariable(name=f'x{i}', lowBound=0) for i in range(1, 10)}
y = {i: LpVariable(name=f'y{i}', cat='Binary') for i in range(1, 10)}

# Add constraints
model += (10 * x[1] + 40 * x[2] + 40 * x[3] + 20 * x[4] + 60 * x[5] +
          40 * x[6] + 15 * x[7] + 30 * x[8] + 45 * x[9] <= 450, "time")

T = 450
model += (x[1] <= y[1] * T, "x1_constraint")
model += (x[2] <= y[2] * T, "x2_constraint")
model += (x[3] <= y[3] * T, "x3_constraint")
model += (x[4] <= y[4] * T, "x4_constraint")
model += (x[5] <= y[5] * T, "x5_constraint")
model += (x[6] <= y[6] * T, "x6_constraint")
model += (x[7] <= y[7] * T, "x7_constraint")
model += (x[8] <= y[8] * T, "x8_constraint")
model += (x[9] <= y[9] * T, "x9_constraint")
model += (y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9] <= 1, "y_constraint")


# Set the objective
model += 47 * x[1] + 90 * x[2] + 210 * x[3] + 59 * x[4] + 239 * x[5] + 95 * x[6] + 52 * x[7] + 33 * x[8] + 50 * x[9]

# Solve the optimization problem
status = model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")

for var in model.variables():
    print(f'{var.name}: {var.value()}')

for name, constraint in model.constraints.items():
    print(f'{name}: {constraint.value()}')
