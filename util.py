# Array for getting 8 surrounding cells
dx = [-1, -1, -1, 0, 1, 1, 1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

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
        elif algo_id == 1:
            print("Brute Force wrong", checked)
        else:
            print("Backtracking wrong", checked)
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

# Check if the assignment 'T' or 'G' of position pos is valid
# We will only check for number cell around the position pos (cause only those are affected)
# If there exists a neighbor number cell around pos that is finished, and the number of trap is wrong --> invalid assignment
# A number cell is finished when the surrounding has no '_' left
def valid_cell(pos, grid, grid_w, grid_h):
    for k in range(8):
        x = pos[0] + dx[k]
        y = pos[1] + dy[k]
        if (not inside_grid(x, y, grid_w, grid_h)) or (not ('0' <= grid[x][y] <= '9')):
            continue
        finished = True
        num_trap = 0
        for i in range(8): 
            if inside_grid(x + dx[i], y + dy[i], grid_w, grid_h):
                if grid[x + dx[i]][y + dy[i]] == 'T':
                    num_trap += 1
                elif grid[x + dx[i]][y + dy[i]] == '_':
                    finished = False
        if finished == True and num_trap != (ord(grid[x][y]) - ord('0')):
            return False
    return True
