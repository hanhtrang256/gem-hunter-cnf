from util import *
from pysat_sol import *
from brute_force_sol import *
from backtrack_sol import *
from grid_generate import *

grid = GRID_GENERATE.generate()

# grid = [['_', '_', '2', '2', '2'],
#         ['_', '_', '2', '_', '_'],
#         ['2', '3', '2', '4', '3'],
#         ['_', '4', '_', '3', '_'],
#         ['2', '_', '_', '_', '_']]
grid_h = len(grid)
grid_w = len(grid[0])

print("Grid generated!")
# Reset grid to run algorithm
reset_grid(grid, grid_w, grid_h)
print_grid(grid, grid_w, grid_h)

cnf = generate_CNF(grid, grid_w, grid_h)

print("#Number of clauses", len(cnf.clauses))
    
# Solution using CNF and pysat to infer the result
PYSAT_SOLUTION.print_solution(grid, grid_w, grid_h, cnf)
check_valid_grid(grid, grid_w, grid_h, 0)
reset_grid(grid, grid_w, grid_h)

# Solution using Backtracking algorithm - check valid grid is in backtrack function
BACKTRACK_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses)
reset_grid(grid, grid_w, grid_h)

# Solution using Brute-Force algorithm
BF_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses)
check_valid_grid(grid, grid_w, grid_h, 1)

