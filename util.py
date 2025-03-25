from pysat.formula import CNF

# Array for getting 8 surrounding cells
dx = [-1, -1, -1, 0, 1, 1, 1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

def get_new_model(model):
    new_model = []
    for i in range(len(model)):
        new_model.append(model[i])
    return new_model

# Reset the grid
def reset_grid(grid, grid_w, grid_h):
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == 'T' or grid[i][j] == 'G':
                grid[i][j] = '_'

# Print the grid
def print_grid(grid, grid_w, grid_h):
    for i in range(grid_h):
        for j in range(grid_w): 
            print(grid[i][j], end = " ")
        print()

# Check valid grid
def check_valid_grid(grid, grid_w, grid_h, algo_id):
    checked = []
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == 'T' or grid[i][j] == 'G' or grid[i][j] == '_':
                continue
            trap_cnt = 0
            for k in range(8):
                if inside_grid(i + dx[k], j + dy[k], grid_w, grid_h) and grid[i + dx[k]][j + dy[k]] == 'T':
                    trap_cnt += 1
            if trap_cnt != (ord(grid[i][j]) - ord('0')):
                checked = [i, j]
    if checked != []:
        if algo_id == 0:
            print("CNF wrong", checked)
            return
        elif algo_id == 1:
            print("Brute Force wrong", checked)
            return
        else:
            print("Backtracking wrong", checked)
            return
    print("Correct")

# Return id of a position in based 1
def get_id(x, y, grid_w): 
    return x * grid_w + y + 1

# Check if cell is inside grid
def inside_grid(x, y, grid_w, grid_h):
    if x < 0 or x >= grid_h or y < 0 or y >= grid_w: 
        return False
    return True

# Get list of unknown cells
def get_unknown_cells(grid, grid_w, grid_h):
    unk_cells = []
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == '_':
                unk_cells.append([i, j])
    return unk_cells

# Every clause true -> return 1
# Some clauses false -> return 0
# Not enough to conclude -> return -1
def check_clause_model(clauses, model):
    hasFalse = False
    not_sure = False
    for i in range(len(clauses)):
        hasTrue = False
        finished = True
        for j in range(len(clauses[i])):
            element = clauses[i][j]
            if (element < 0 and model[-element] == False) or (element > 0 and model[element] == True):
                hasTrue = True
                finished = True
                break
            if model[abs(element)] == None:
                finished = False
        if finished and not hasTrue:
            hasFalse = True
            break
        if not finished:
            not_sure = True
    
    # ∃ false clause --> return False
    if hasFalse == True:
        return 0
    
    # ∀ clauses are finished and no false clause --> result found --> return True (early termination)
    if not_sure == False:
        return 1
    return -1

# Get new disjunction at position (i, j)
def get_new_disjunc(i, j, mask, bit_want, sign, grid_w, grid_h):
    if mask.bit_count() != bit_want:
        return []
    new_disjunc = []
    valid_disjunc = True
    for k in range(8): 
        if (mask & (1 << k)) > 0:
            new_x = i + dx[k] 
            new_y = j + dy[k]
            if not inside_grid(new_x, new_y, grid_w, grid_h):
                valid_disjunc = False
                return []
            new_disjunc.append(sign * get_id(new_x, new_y, grid_w))
    return new_disjunc

# Generate all the disjuncs of all positions and add them all to form
# conjunctive normal form. Factoring is added before adding new disjuncts to CNF.
# Suppose n positions around
# Current position not trap --> add [¬cur]
# at least k traps = at most n - k non-trap
# At most n - k non-trap --> add [(X1 ∨ X2 ∨ ... ∨ X(n-k+1)) ∧ ...] (all combinations of n - k + 1 elements)

# at most k traps = ¬(at least k + 1 traps)
# (X1 ∧ X2 ∧ ... ∧ X(k+1)) ∨ ... (all combinations of k+1 elements)
# ¬((X1 ∧ X2 ∧ ... ∧ X(k+1)) ∨ ...)
# ¬(X1 ∧ X2 ∧ ... ∧ X(k+1)) ∧ ¬(...) 
# add [(¬X1 ∨ ¬X2 ∨ ... ∨ X(k+1)) ∧ (...)]
def generate_CNF(grid, grid_w, grid_h):
    cnf = CNF()
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == '_':
                continue
            # First, add to the knowledge base that the current position is not trap
            cnf.append([-1 * get_id(i, j, grid_w)])
            num_trap = ord(grid[i][j]) - ord('0')
            num_valid_pos = 0
            for k in range(8):
                if inside_grid(i + dx[k], j + dy[k], grid_w, grid_h):
                    num_valid_pos += 1
            for mask in range(2 ** 8):
                # Find CNF "at least #num_trap trap cells"
                # This sentence equates to "at most #(num_valid_pos - num_trap) not-trap cell"
                new_disjunc = get_new_disjunc(i, j, mask, num_valid_pos - num_trap + 1, 1, grid_w, grid_h)
                if new_disjunc != []:
                    cnf.append(new_disjunc)
                # Find CNF "at most #num_trap traps"
                # This sentence is a negation of "at lease #num_trap trap cells"
                new_disjunc = get_new_disjunc(i, j, mask, num_trap + 1, -1, grid_w, grid_h)
                if new_disjunc != []:
                    cnf.append(new_disjunc)
    
    # Remove duplicate clauses
    seen = set()
    cnf.clauses = [clause for clause in cnf.clauses if frozenset(clause) not in seen and not seen.add(frozenset(clause))]
    return cnf