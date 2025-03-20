from util import *
from cnf_sol import *
from brute_force_sol import *
from backtrack_sol import *
from grid_generate import *

# grid = [['2', '_', '_', '1', '_'],
#         ['_', '5', '4', '2', '_'],
#         ['3', '_', '_', '2', '1'],
#         ['3', '_', '6', '_', '1'],
#         ['2', '_', '_', '2', '1']]
 
# grid = [['3', '_', '2', '_'],
#         ['_', '_', '2', '_'],
#         ['_', '3', '1', '_']]

grid = GRID_GENERATE.generate()
grid_h = len(grid)
grid_w = len(grid[0])

print("Grid generated!")
print_grid(grid, grid_w, grid_h)

# Reset grid to run algorithm
reset_grid(grid, grid_w, grid_h)

# Solution using CNF and pysat to infer the result
CNF_SOLUTION.print_solution(grid, grid_w, grid_h)

check_valid_grid(grid, grid_w, grid_h, 0)
reset_grid(grid, grid_w, grid_h)

# Solution using Brute-Force algorithm
BF_SOLUTION.print_solution(grid, grid_w, grid_h)

check_valid_grid(grid, grid_w, grid_h, 1)
reset_grid(grid, grid_w, grid_h)

# Solution using Backtracking algorithm - check valid grid is in backtrack function
BACKTRACK_SOLUTION.print_solution(grid, grid_w, grid_h)
