from util import *
from collections import deque

pure_symbols = deque()


# A class for backtracking solution
# Recursively assign value for each unknown cell, it found invalid case => backtrack and reassign new value.
# This backtrack solution returns the first solution it found and stop running.
class BACKTRACK_SOLUTION:
    found = False

    @staticmethod
    def backtrack(grid, grid_w, grid_h, index, unk_cells, clauses, model):
        # Early check --> if can early termination
        early_check = check_clause_model(clauses, model)
        if early_check == 0:
            return False

        if early_check == 1:
            BACKTRACK_SOLUTION.found = True
            
            for i in range(grid_h):
                for j in range(grid_w): 
                    if grid[i][j] == '_': 
                        compress_id = get_id(i, j, grid_w)
                        if model[compress_id] == None or model[compress_id] == False:
                            grid[i][j] = 'G'
                        elif model[compress_id] == True:
                            grid[i][j] = 'T'
            
            print_grid(grid, grid_w, grid_h)
            check_valid_grid(grid, grid_w, grid_h, 2)

            return True

        # Get id of position
        pos = unk_cells[index]
        compress_id = get_id(pos[0], pos[1], grid_w)

        # If already assigned
        if model[compress_id] != None:
            return BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, model)
        
        # Try T
        if BACKTRACK_SOLUTION.found == False:
            model[compress_id] = True 
            res_T = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, model)
            model[compress_id] = None

            if res_T:
                return True

        # Try G
        if BACKTRACK_SOLUTION.found == False:
            model[compress_id] = False
            res_G = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, model)
            model[compress_id] = None

            if res_G:
                return True

        return BACKTRACK_SOLUTION.found
    
    @staticmethod
    def print_solution(grid, grid_w, grid_h, clauses):
        use_clauses = []
        for i in range(len(clauses)): 
            arr = []
            for j in range(len(clauses[i])):
                arr.append(clauses[i][j])
            use_clauses.append(arr)

        # Get lists of unknown cells
        unk_cells = get_unknown_cells(grid, grid_w, grid_h)
        num_unk_cell = len(unk_cells)

        model = [None] * (grid_w * grid_h + 1)

        # Preassign the known variables first (number cell is obviously not a trap)
        for i in range(grid_h):
            for j in range(grid_w):
                if '0' <= grid[i][j] <= '9':
                    model[get_id(i, j, grid_w)] = False

        found_sol = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, 0, unk_cells, use_clauses, model)
        if found_sol:
            print("Backtrack found a solution")
        else:
            print("Backtrack cannot find a solution")