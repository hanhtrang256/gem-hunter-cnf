from util import *

# A class for brute-force solution
# Since we will go through all possible "worlds", which in this game is 2^N cases (N: number of unknown cells)
# So I use a bit-generating methods to generate all 2^N possible masks.
# Define 0 as non-trap cell (G) and 1 as trap cell (T).
class BF_SOLUTION:
    @staticmethod
    def print_solution(grid, grid_w, grid_h):
        # Get lists of unknown cells
        unk_cells = get_unknown_cells(grid, grid_w, grid_h)
        num_unk_cell = len(unk_cells)

        # Generate all masks
        for mask in range(2 ** num_unk_cell):
            # Reset grid for new-mask assigment
            for i in range(num_unk_cell): 
                pos = unk_cells[i]
                grid[pos[0]][pos[1]] = '_'

            # Assign variables based on current mask
            valid_state = True
            for i in range(num_unk_cell):
                pos = unk_cells[i]
                if (mask & (1 << i)) > 0:
                    grid[pos[0]][pos[1]] = 'T'
                else:
                    grid[pos[0]][pos[1]] = 'G'

                # Check each position during assignment will reduct the time complexity
                # No need to check for whole grid, but only those that are affected by the new assignment
                if not valid_cell(pos, grid, grid_w, grid_h): 
                    valid_state = False
                    break
            
            # If found a solution, then print
            if valid_state:
                print("Complete board solver Brute-Force!")
                print_grid(grid, grid_w, grid_h)
                return

        # In case there is no solution
        print("Brute-force cannot find any valid combinations!")
