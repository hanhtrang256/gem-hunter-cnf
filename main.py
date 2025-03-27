from grid_function import *
from cnf_function import *
from pysat_sol import *
from brute_force_sol import *
from backtrack_sol import *
from grid_generate import *

# Read grid from file
id_file = 6
grid = read_grid_file(f'testcases/input_{id_file}.txt')
grid_h = len(grid)
grid_w = len(grid[0]) 
print_grid(grid, grid_w, grid_h)

# Generate the CNF clauses. Duplicate clauses are removed inside the function.
cnf = generate_CNF(grid, grid_w, grid_h)

print("# Number of clauses", len(cnf.clauses))

fout = open(str(f'testcases/output_{id_file}.txt'), "a")
# Solution using CNF and pysat to infer the result
PYSAT_SOLUTION.print_solution(grid, grid_w, grid_h, cnf, fout)
check_valid_grid(grid, grid_w, grid_h, 0)
reset_grid(grid, grid_w, grid_h)
fout.write("\n")

# Solution using Backtracking algorithm - check valid grid is in backtrack function
BACKTRACK_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses, fout)
reset_grid(grid, grid_w, grid_h)
fout.write("\n")

# Solution using Brute-Force algorithm
BF_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses, fout)
check_valid_grid(grid, grid_w, grid_h, 1)

fout.close()
