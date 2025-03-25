from util import *

# A class for brute-force solution
# Since we will go through all possible "worlds", which in this game is 2^N cases (N: number of unknown cells)
# So I use a bit-generating methods to generate all 2^N possible masks.
# Define 0 as trap cell (T) and 1 as gem cell (G).
class BF_SOLUTION:
    @staticmethod
    def print_solution(grid, grid_w, grid_h, clauses):
        use_clauses = []
        for i in range(len(clauses)): 
            arr = []
            for j in range(len(clauses[i])):
                arr.append(clauses[i][j])
            use_clauses.append(arr)
        
        # print(use_clauses)

        # Get lists of unknown cells
        unk_cells = get_unknown_cells(grid, grid_w, grid_h)
        num_unk_cell = len(unk_cells)

        model = [None] * (grid_w * grid_h + 1)

        # Preassign the known variables first (number cell is obviously not a trap)
        for i in range(grid_h):
            for j in range(grid_w):
                if '0' <= grid[i][j] <= '9':
                    model[get_id(i, j, grid_w)] = False

        # Generate all masks
        for mask in range(2 ** len(unk_cells)):
            # Reset grid for new-mask assigment
            for index in range(len(unk_cells)): 
                pos = unk_cells[index]
                model[get_id(pos[0], pos[1], grid_w)] = None

            valid_assignment = True

            # Assign variables based on current mask
            for index in range(len(unk_cells)):
                pos = unk_cells[index]
                compress_id = get_id(pos[0], pos[1], grid_w)
                if (mask & (1 << index)) > 0:
                    model[compress_id] = False
                else:
                    model[compress_id] = True

            # Early check --> if can early termination
            early_check = check_clause_model(clauses, model)

            if early_check == 1:
                print("Complete board solver Brute-Force!")
                for i in range(grid_w):
                    for j in range(grid_h):
                        if grid[i][j] == '_':
                            compress_id = get_id(i, j, grid_w)
                            if model[compress_id] == None or model[compress_id] == False:
                                grid[i][j] = 'G'
                            elif model[compress_id] == True:
                                grid[i][j] = 'T'
                print_grid(grid, grid_w, grid_h)
                return

        # In case there is no solution
        print("Brute-force cannot find any valid combinations!")
