from util import *
import random
grid_width = 5
grid_height = 5
num_traps = 7
num_gems = 3

def get_random(low, high):
    return random.randint(low, high)

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
            for i in range(num_traps):
                x = get_random(0, grid_height - 1)
                y = get_random(0, grid_width - 1)

                if grid[x][y] == '_':
                    grid[x][y] = 'T'
                else:
                    i -= 1
            
            # Place the gems
            for i in range(num_gems):
                x = get_random(0, grid_height - 1)
                y = get_random(0, grid_width - 1)

                if grid[x][y] == '_':
                    grid[x][y] = 'G'
                else:
                    i -= 1
            
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