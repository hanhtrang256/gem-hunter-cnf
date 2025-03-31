from grid_function import *
from pysat.formula import CNF

# This function checks if the CNF is satisfied in the current model
# All clauses true -> return 1
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
    
    # ∀ clauses are finished and no false clause --> result found --> return True 
    if not_sure == False:
        return 1

    # Not decideable
    return -1

# Check if the clauses is true in the current mask (a model)
def check_clause_mask(clauses, mask, empty_id):
    for clause in clauses:
        hasTrue = False
        for literal in clause:
            if empty_id[abs(literal)] == None:
                continue
            if literal > 0 and (mask & (1 << empty_id[literal]) > 0):
                hasTrue = True
                break
            elif literal < 0 and not (mask & (1 << empty_id[-literal])):
                hasTrue = True
                break
        if not hasTrue:
            return False
    return True

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

# Optimize the CNF clauses by assigning some known information in the knowledge base
# and delete the clauses that are already true
def optimize_clause(grid, grid_w, grid_h, clauses, model):
    clauses_contain = [[]] * (grid_w * grid_h + 2)
    deleted = [False] * (len(clauses) + 2)

    for i in range(len(clauses)):
        for var in clauses[i]:
            clauses_contain[abs(var)].append(i)

    # Preassign the known variables first (number cell is obviously not a trap)
    for i in range(grid_h):
        for j in range(grid_w):
            if '0' <= grid[i][j] <= '9':
                element = get_id(i, j, grid_w)
                model[element] = False
                for id in clauses_contain[element]:
                    if deleted[id] == True:
                        continue
                    hasTrue = False
                    for var in clauses[id]:
                        if (var < 0 and model[-var] == False) or (var > 0 and model[var] == True): 
                            hasTrue = True
                            break
                    if hasTrue == True:
                        deleted[id] = True
    
    # New clause
    new_clause = [] 
    for i in range(len(clauses)): 
        if deleted[i]:
            continue
        clause = []
        for var in clauses[i]:
            clause.append(var)
        new_clause.append(clause)
    
    return new_clause