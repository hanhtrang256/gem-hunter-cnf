from util import *
# the standard way to import PySAT:
from pysat.formula import CNF
from pysat.solvers import Solver

# Suppose n positions around
# Current position not trap --> add [¬cur]
# at least k traps = at most n - k non-trap
# At most n - k non-trap --> add [(X1 ∨ X2 ∨ ... ∨ X(n-k+1)) ∧ ...] (all combinations of n - k + 1 elements)

# at most k traps = ¬(at least k + 1 traps)
# (X1 ∧ X2 ∧ ... ∧ X(k+1)) ∨ ... (all combinations of k+1 elements)
# ¬((X1 ∧ X2 ∧ ... ∧ X(k+1)) ∨ ...)
# ¬(X1 ∧ X2 ∧ ... ∧ X(k+1)) ∧ ¬(...) 
# add [(¬X1 ∨ ¬X2 ∨ ... ∨ X(k+1)) ∧ (...)]
class CNF_SOLUTION:
    cnf = CNF()

    @staticmethod
    # Get new disjunc at position (i, j)
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

    @staticmethod
    # Generate all the disjuncs of all positions and add them all to form
    # conjunctive normal form
    def generate_CNF(grid, grid_w, grid_h):
        for i in range(grid_h):
            for j in range(grid_w):
                if grid[i][j] == '_':
                    continue
                # First, add to the knowledge base that the current position is not trap
                CNF_SOLUTION.cnf.append([-1 * get_id(i, j, grid_w)])
                num_trap = ord(grid[i][j]) - ord('0')
                num_valid_pos = 0
                for k in range(8):
                    if inside_grid(i + dx[k], j + dy[k], grid_w, grid_h):
                        num_valid_pos += 1
                for mask in range(2 ** 8):
                    # Find CNF "at least #num_trap trap cells"
                    # This sentence equates to "at most #(num_valid_pos - num_trap) not-trap cell"
                    new_disjunc = CNF_SOLUTION.get_new_disjunc(i, j, mask, num_valid_pos - num_trap + 1, 1, grid_w, grid_h)
                    if new_disjunc != []:
                        CNF_SOLUTION.cnf.append(new_disjunc)
                    # Find CNF "at most #num_trap traps"
                    # This sentence is a negation of "at lease #num_trap trap cells"
                    new_disjunc = CNF_SOLUTION.get_new_disjunc(i, j, mask, num_trap + 1, -1, grid_w, grid_h)
                    if new_disjunc != []:
                        CNF_SOLUTION.cnf.append(new_disjunc)

    @staticmethod
    # Print out solution
    def print_solution(grid, grid_w, grid_h):
        CNF_SOLUTION.generate_CNF(grid, grid_w, grid_h)
        print(CNF_SOLUTION.cnf.clauses)

        solver = Solver(bootstrap_with = CNF_SOLUTION.cnf)
        if solver.solve():
            print("Satisfied")
            model = solver.get_model()
            print("model", model)

            print("Complete board solver CNF!")
            for i in range(grid_h):
                for j in range(grid_w):
                    if grid[i][j] == '_':
                        if get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] > 0:
                            grid[i][j] = 'T'
                        elif get_id(i, j, grid_w) <= len(model) and model[get_id(i, j, grid_w) - 1] < 0:
                            grid[i][j] = 'G'
                        else:
                            grid[i][j] = 'G'
                    print(grid[i][j], end = " ")
                print()
        else:
            print("Unsatisfied")


