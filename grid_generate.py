from util import *
import random
grid_width = 20
grid_height = 20
num_traps = 180
num_gems = 20

def get_random(low, high):
    return random.randint(low, high)

# A class to generate a valid map with given size and number of traps, gems. 
class GRID_GENERATE:
    @staticmethod
    def generate():
        while True:
            grid = []
            # Empty the grid 
            for i in range(grid_height):
                col = []
                for j in range(grid_width):
                    col.append('_')
                grid.append(col)

            # Place the traps
            cnt = 0
            while cnt < num_traps:
                x = get_random(0, grid_height - 1)
                y = get_random(0, grid_width - 1)

                if grid[x][y] == '_':
                    grid[x][y] = 'T'
                    cnt += 1
            
            # Place the gems
            cnt = 0
            while cnt < num_gems:
                x = get_random(0, grid_height - 1)
                y = get_random(0, grid_width - 1)

                if grid[x][y] == '_':
                    grid[x][y] = 'G'
                    cnt += 1

            # Place the numbers
            for i in range(grid_height):
                for j in range(grid_width):
                    if grid[i][j] == 'T' or grid[i][j] == 'G':
                        continue
                    trap_cnt = 0
                    for k in range(8):
                        if inside_grid(i + dx[k], j + dy[k], grid_width, grid_height) and grid[i + dx[k]][j + dy[k]] == 'T':
                            trap_cnt += 1
                    if trap_cnt > 0:
                        grid[i][j] = chr(ord('0') + trap_cnt)
            
            return grid