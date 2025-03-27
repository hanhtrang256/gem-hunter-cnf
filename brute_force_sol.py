from grid_function import *
from cnf_function import *
import time

# A class for brute-force solution
# Since we will go through all possible "worlds", which in this game is 2^N cases (N: number of unknown cells)
# So I use a bit-generating methods to generate all 2^N possible masks.
# Define 0 as trap cell (T) and 1 as gem cell (G).
class BF_SOLUTION:
    # Print the solution
    @staticmethod
    def print_solution(grid, grid_w, grid_h, clauses, fout):
        if grid_w > 6 and grid_h > 6:
            fout.write("Brute force took too long to solve!\n")
            return
        # Convert the CNF clauses to list of arrays for convenient usage
        use_clauses = []
        for i in range(len(clauses)): 
            arr = []
            for j in range(len(clauses[i])):
                arr.append(clauses[i][j])
            use_clauses.append(arr)

        # Get lists of unknown cells
        unk_cells = get_unknown_cells(grid, grid_w, grid_h)
        num_unk_cell = len(unk_cells)

        # Initialize model
        model = [None] * (grid_w * grid_h + 1)
        
        # Delete unnecessary clauses
        use_clauses = optimize_clause(grid, grid_w, grid_h, use_clauses, model)

        # Generate all masks
        start_time = time.time()
        for mask in range(2 ** len(unk_cells) - 1, -1, -1):
            # Reset grid for new-mask assigment
            for index in range(len(unk_cells)): 
                pos = unk_cells[index]
                model[get_id(pos[0], pos[1], grid_w)] = None

            # Assign variables based on current mask
            for index in range(len(unk_cells)):
                pos = unk_cells[index]
                compress_id = get_id(pos[0], pos[1], grid_w)
                if (mask & (1 << index)) > 0:
                    model[compress_id] = True
                else:
                    model[compress_id] = False

            # Check if found valid model 
            check = check_clause_model(clauses, model)

            if check == 1:
                end_time = time.time()
                time_taken = end_time - start_time
                fout.write("Complete board solver by Brute-Force!\n")
                for i in range(grid_w):
                    for j in range(grid_h):
                        if grid[i][j] == '_':
                            compress_id = get_id(i, j, grid_w)
                            if model[compress_id] == None or model[compress_id] == False:
                                grid[i][j] = 'G'
                            elif model[compress_id] == True:
                                grid[i][j] = 'T'
                        fout.write(grid[i][j] + ' ')
                    fout.write("\n")
                fout.write(f'Time taken BRUTE-FORCE: {time_taken: .6f} seconds!\n')
                return

        # In case there is no solution
        fout.write("Brute-force cannot find any valid combinations!\n")
