from util import *

# A class for backtracking solution
# Recursively assign value for each unknown cell, it found invalid case => backtrack and reassign new value.
# This backtrack solution returns the first solution it found and stop running.
class BACKTRACK_SOLUTION:
    found = False

    @staticmethod
    # Backtrack to find answer
    def backtrack(i, num_unk_cell, unk_cells, grid, grid_w, grid_h):
        # Reach a solution - because checking valid is performed during assignment, so if can reach to the end,
        # then this is a solution
        if i >= num_unk_cell:
            BACKTRACK_SOLUTION.found = True
            print("Complete board solver Backtrack!")
            print_grid(grid, grid_w, grid_h)

            check_valid_grid(grid, grid_w, grid_h, 2)
            return

        pos = unk_cells[i]

        # try T
        if not BACKTRACK_SOLUTION.found:
            grid[pos[0]][pos[1]] = 'T'
            if valid_cell(pos, grid, grid_w, grid_h):
                BACKTRACK_SOLUTION.backtrack(i + 1, num_unk_cell, unk_cells, grid, grid_w, grid_h)

        # try G
        if not BACKTRACK_SOLUTION.found:    
            grid[pos[0]][pos[1]] = 'G'
            if valid_cell(pos, grid, grid_w, grid_h):
                BACKTRACK_SOLUTION.backtrack(i + 1, num_unk_cell, unk_cells, grid, grid_w, grid_h)
        
        grid[pos[0]][pos[1]] = '_'
    
    @staticmethod
    def print_solution(grid, grid_w, grid_h):
        # Get lists of unknown cells
        unk_cells = get_unknown_cells(grid, grid_w, grid_h)
        num_unk_cell = len(unk_cells)

        BACKTRACK_SOLUTION.backtrack(0, num_unk_cell, unk_cells, grid, grid_w, grid_h)

        if BACKTRACK_SOLUTION.found == False:
            print("Backtrack cannot find any solution!")