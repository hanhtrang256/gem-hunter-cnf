from util import *
from pysat.solvers import Solver
import time

# A class that uses the pysat library to solve the CNF clauses
class PYSAT_SOLUTION:
    @staticmethod
    # Print out solution
    def print_solution(grid, grid_w, grid_h, cnf):
        start_time = time.time()
        solver = Solver(bootstrap_with = cnf)
        if solver.solve():
            print("Satisfied")
            model = solver.get_model()
            end_time = time.time()

            time_taken = end_time - start_time
            print(f'Complete board solver CNF! Time taken PYSAT: {time_taken:.6f} seconds!')
            for i in range(grid_h):
                for j in range(grid_w):
                    if grid[i][j] == '_':
                        if get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] > 0:
                            grid[i][j] = 'T'
                        elif get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] < 0:
                            grid[i][j] = 'G'
                        else:
                            grid[i][j] = 'G'
                    print(grid[i][j], end = " ")
                print()
        else:
            print("Unsatisfied")


