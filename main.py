from variable import *
from constraint import *
from constraint import Constraint_difference_var_var
from problem import Problem

import time

if __name__ == "__main__":

	#being recording the time taken to run the solution
	startTime = time.time()

	#create a new problem and begin to solve recursively
	prob = Problem()
	prob.solve()

	#Print the number of solutions found and the time taken to solve
	print("Number of solutions found:", Problem.no_of_solutions)
	print("Time taken", time.time() - startTime)

