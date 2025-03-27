# Array for getting 8 surrounding cells
dx = [-1, -1, -1, 0, 1, 1, 1, 0]
dy = [-1, 0, 1, 1, 1, 0, -1, -1]

# Read the grid from file
def read_grid_file(filename):
    with open(str(filename)) as f:
        row, col = [int(x) for x in next(f).split()] # Read number of rows and columns at first line
        grid = []
        for line in f:
            grid.append([x for x in line.split()]) # Read each element of grid
    return grid

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

# Check if an assignment for grid is valid
def check_valid_grid(grid, grid_w, grid_h, algo_id):
    if algo_id == 1 and grid_w > 6 and grid_h > 6:
        print("Brute Force took too long")
        return
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
    if algo_id == 0:
        print("Pysat", end=" ")
    elif algo_id == 1:
        print("Brute Force", end=" ")
    else:
        print("Backtracking", end=" ")
    if checked != []:
        print("wrong", checked)
        return
    print("finished and is correct!")

# Return id of a position in based 1
def get_id(x, y, grid_w): 
    return x * grid_w + y + 1

# Check if a cell (x, y) is inside grid
def inside_grid(x, y, grid_w, grid_h):
    if x < 0 or x >= grid_h or y < 0 or y >= grid_w: 
        return False
    return True

# Get list of unknown cells (cells with '_')
def get_unknown_cells(grid, grid_w, grid_h):
    unk_cells = []
    for i in range(grid_h):
        for j in range(grid_w):
            if grid[i][j] == '_':
                unk_cells.append([i, j])
    return unk_cells