from grid_function import *
from cnf_function import *
import time

# A class for backtracking solution
# Recursively assign value for each unknown cell and apply early check
# If early invalid/valid (clauses/model) => return
# This backtrack solution will not continue assigning after it has found the first solution
class BACKTRACK_SOLUTION:
    found = False # found = True => solution has been found --> no further search needed.

    # Get new model for backtracking
    def get_new_model(model):
        new_model = []
        for i in range(len(model)):
            new_model.append(model[i])
        return new_model

    # Find and return unit clause if exist
    def find_unit_clause(clauses, model):
        unit_clause = None
        for clause in clauses:
            finished = True
            unassigned = 0
            unassigned_var = None
            for var in clause:
                if (var < 0 and model[-var] == False) or (var > 0 and model[var] == True):
                    finished = True
                    break
                if model[abs(var)] == None:
                    finished = False
                    unassigned += 1
                    unassigned_var = var
            if finished:
                continue
            if unassigned == 1:
                unit_clause = unassigned_var
                break
        return unit_clause

    # Find pure symbols if exist
    def find_pure_symbol(clauses, model):
        pos = [0] * (len(model) + 2)
        neg = [0] * (len(model) + 2)
        unfinished = 0
        for clause in clauses:
            finished = False
            for var in clause:
                if (var < 0 and model[-var] == False) or (var > 0 and model[var] == True):
                    finished = True
                    break
            if not finished: 
                unfinished += 1
                for var in clause:
                    if model[abs(var)] == None:
                        if var > 0: 
                            pos[var] += 1
                        else:
                            neg[-var] += 1
        pure_symbols = []
        for i in range(len(model) + 1):
            if pos[i]*neg[i]==0 and pos[i]+neg[i]>0 and pos[i]+neg[i]==unfinished:
                # return i if pos[i] > 0 else -i
                pure_symbols.append(i if pos[i] > 0 else -i)
        return pure_symbols

    # Backtracking
    def backtrack(grid, grid_w, grid_h, index, unk_cells, clauses, model, fout):
        # Early check --> if can early termination
        early_check = check_clause_model(clauses, model)
        if early_check == 0:
            return False

        if early_check == 1:
            BACKTRACK_SOLUTION.found = True
            fout.write("Complete board solver by Backtrack!\n")
            for i in range(grid_h):
                for j in range(grid_w): 
                    if grid[i][j] == '_': 
                        compress_id = get_id(i, j, grid_w)
                        if model[compress_id] == None or model[compress_id] == False:
                            grid[i][j] = 'G'
                        elif model[compress_id] == True:
                            grid[i][j] = 'T'
                    fout.write(grid[i][j] + ' ')
                fout.write('\n')
            # check_valid_grid(grid, grid_w, grid_h, 2)

            return True

        # Unit clause heuristic (propagation if possible)
        unit_clause = BACKTRACK_SOLUTION.find_unit_clause(clauses, model)
        if unit_clause != None:
            new_model = BACKTRACK_SOLUTION.get_new_model(model)
            if unit_clause > 0: 
                new_model[unit_clause] = True
            else:
                new_model[-unit_clause] = False
            
            res_unit = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index, unk_cells, clauses, new_model, fout)
            return res_unit

        # Pure symbol heuristic
        pure_symbols = BACKTRACK_SOLUTION.find_pure_symbol(clauses, model)
        if pure_symbols != []:
            new_model = BACKTRACK_SOLUTION.get_new_model(model)
            for var in pure_symbols:
                new_model[abs(var)] = True if var > 0 else False
            res_pure = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index, unk_cells, clauses, new_model, fout)

        # Get id of position
        pos = unk_cells[index]
        compress_id = get_id(pos[0], pos[1], grid_w)

        # If already assigned by previous heuristic usage
        if model[compress_id] != None:
            res_already = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, model, fout)
            return res_already
        
        # Try T if not yet found solution
        if BACKTRACK_SOLUTION.found == False:
            new_model = BACKTRACK_SOLUTION.get_new_model(model)
            new_model[compress_id] = True 
            res_T = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, new_model, fout)

            if res_T:
                return True

        # Try G if not yet found solution
        if BACKTRACK_SOLUTION.found == False:
            new_model = BACKTRACK_SOLUTION.get_new_model(model)
            new_model[compress_id] = False 
            res_G = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, index + 1, unk_cells, clauses, new_model, fout)

            if res_G:
                return True

        return BACKTRACK_SOLUTION.found
    
    # Print the solution
    def print_solution(grid, grid_w, grid_h, clauses, fout):
        BACKTRACK_SOLUTION.found = False
        # Convert the CNF clauses to lists of arrays for convenient usage
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
        
        start_time = time.time()
        found_sol = BACKTRACK_SOLUTION.backtrack(grid, grid_w, grid_h, 0, unk_cells, use_clauses, model, fout)
        end_time = time.time()
        time_taken = end_time - start_time
        # print(f"Time taken {time_taken:.4f} second")
        time_taken *= 1000
        fout.write(f'{time_taken:.4f} ms!\n')
