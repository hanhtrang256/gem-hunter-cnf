# from util.grid_function import *
# from util.cnf_function import *
from util import *
from algorithm import *
# from pysat_sol import *
# from brute_force_sol import *
# from backtrack_sol import *
from grid_generate import *
import sys

NFILE = 6

def solve(id_file):
    print(f'File input_{id_file} is read!', end=" ")
    # Read grid from file
    grid = read_grid_file(f'../testcases/input_{id_file}.txt')
    grid_h = len(grid)
    grid_w = len(grid[0]) 

    num_empty = 0
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == '_':
                num_empty += 1

    # Generate the CNF clauses. Duplicate clauses are removed inside the function.
    cnf = generate_CNF(grid, grid_w, grid_h)

    fout = open(str(f'../testcases/output_{id_file}.txt'), "w")
    fout.write(f'{grid_h} x {grid_w}\n')
    fout.write(f'{len(cnf.clauses)} clauses!\n')
    fout.write(f'{num_empty} empty cells!\n')
    
    # Solution using CNF and pysat to infer the result
    PYSAT_SOLUTION.print_solution(grid, grid_w, grid_h, cnf, fout)
    reset_grid(grid, grid_w, grid_h)
    fout.write("\n")

    # Solution using Backtracking algorithm - check valid grid is in backtrack function
    BACKTRACK_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses, fout)
    reset_grid(grid, grid_w, grid_h)
    fout.write("\n")

    # Solution using Brute-Force algorithm
    BF_SOLUTION.print_solution(grid, grid_w, grid_h, cnf.clauses, fout)
    reset_grid(grid, grid_w, grid_h)

    fout.close()
    print("-> Done!")

if len(sys.argv) >= 2: 
    get_id_argv = sys.argv[1]
    id_file = ord(get_id_argv) - ord('0')
    solve(id_file)
else:
    # solve(2)
    for i in range(1, NFILE + 1):
        solve(i)