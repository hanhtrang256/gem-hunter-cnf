from grid_function import *
from cnf_function import *
import time

# A class for brute-force solution
# Since we will go through all possible "worlds", which in this game is 2^N cases (N: number of unknown cells)
# So I use a bit-generating methods to generate all 2^N possible masks.
# Define 1 as trap cell (T) and 0 as gem cell (G).
class BF_SOLUTION:
    def next_mask(x):
        smallest = x & -x  
        ripple = x + smallest
        new_mask = (((ripple ^ x) >> 2) // smallest) | ripple
        return new_mask

    def print_solution(grid, grid_w, grid_h, clauses, fout): 
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

        if num_unk_cell > 25:
            fout.write("Brute Force took too long to solve!\n")
            return

        model = [None] * (grid_w * grid_h + 2)
        
        # Delete unnecessary clauses
        use_clauses = optimize_clause(grid, grid_w, grid_h, use_clauses, model)

        empty_id = [None] * (grid_w * grid_h + 2)
        id = 0
        for i in range(grid_h):
            for j in range(grid_w):
                if grid[i][j] == '_': 
                    empty_id[get_id(i, j, grid_w)] = id
                    id += 1

        start_time = time.time()
        for num_traps in range(num_unk_cell, - 1, -1):
            mask = (1 << num_traps) - 1
            while mask < (1 << num_unk_cell):
                if check_clause_mask(use_clauses, mask, empty_id):
                    fout.write("Complete board solver by Brute-Force!\n")
                    end_time = time.time()
                    time_taken = (end_time - start_time) * 1000
                    for i in range(grid_w):
                        for j in range(grid_h):
                            if grid[i][j] == '_':
                                compress_id = get_id(i, j, grid_w)
                                if not (mask & (1 << empty_id[compress_id])):
                                    grid[i][j] = 'G'
                                elif (mask & (1 << empty_id[compress_id])):
                                    grid[i][j] = 'T'
                            fout.write(grid[i][j] + ' ')
                        fout.write("\n")
                    fout.write(f'{time_taken:.4f} ms!\n')
                    return
                mask = BF_SOLUTION.next_mask(mask)
        # In case there is no solution
        fout.write("Brute-force cannot find any valid combinations!\n")