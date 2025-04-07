from util import *
from pysat.solvers import Solver
import time

# A class that uses the pysat library to solve the CNF clauses
class PYSAT_SOLUTION:
    # Print out solution
    def print_solution(grid, grid_w, grid_h, cnf, fout):
        dupl = find_dup_clauses(cnf.clauses)
        if dupl != None:
            print("Duplicate clauses detected", dupl)
        start_time = time.time()
        solver = Solver(bootstrap_with = cnf)

        if solver.solve():
            end_time = time.time()
            model = solver.get_model()
            time_taken = (end_time - start_time) * 1000
            fout.write("Complete board solver by PYSAT!\n")
            for i in range(grid_h):
                for j in range(grid_w):
                    if grid[i][j] == '_':
                        if get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] > 0:
                            grid[i][j] = 'T'
                        elif get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] < 0:
                            grid[i][j] = 'G'
                        else:
                            grid[i][j] = 'G'
                    fout.write(grid[i][j] + ' ')
                fout.write("\n")
            fout.write(f'{time_taken:.4f} ms!\n')
        else:
            fout.write("PYSAT cannot find solution. Unsatisfied CNF!\n")


