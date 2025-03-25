from util import *
from pysat.solvers import Solver

class PYSAT_SOLUTION:
    @staticmethod
    # Print out solution
    def print_solution(grid, grid_w, grid_h, cnf):
        # Check for duplicate clauses (in terms of safety only)
        dup_clause = False
        for i in range(len(cnf.clauses)):
            for j in range(i + 1, len(cnf.clauses)):
                if cnf.clauses[i] == cnf.clauses[j]: 
                    print("Dup clauses", cnf.clauses[i], cnf.clauses[j])

        solver = Solver(bootstrap_with = cnf)
        if solver.solve():
            print("Satisfied")
            model = solver.get_model()
            # print("model", model)

            print("Complete board solver CNF!")
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


