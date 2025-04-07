import main

# Print n spaces
def print_space(fout, n):
    for i in range(n):
        fout.write(" ")

# Print header line to separate test cases
def print_header_line(fout):
    fout.write('|')
    for i in range(len("|    Grid size    |    # Clauses    |    # Empty cells    |     Algorithm     |    Time         |") - 2):
        fout.write('-')
    fout.write('|\n')

# Print the statistic for each algorithm
def print_algo(fout, row, col, nclauses, empty_cells, time, algo_name):
    offset = 4
    fout.write(f'|    {row}x{col}')
    print_space(fout, len("Grid size") - len(row) - len(col) - 1 + offset)
    
    fout.write(f'|    {nclauses}')
    print_space(fout, len("# Clauses") - len(nclauses) + offset)

    fout.write(f'|    {empty_cells}')
    print_space(fout, len("# Empty cells") - len(empty_cells) + offset)

    fout.write(f'|     {algo_name}')
    add = len("Algorithm") - len(algo_name)
    print_space(fout, add + offset + 1)

    if time == None:
        time = "Long"
    else:
        time += "ms"
    fout.write(f'|    {time}')
    add = len("Time") - len(time)
    print_space(fout, add + offset + 5)
    fout.write("|\n")

# Print the experiments into the statistics.txt file
def show_experiments():
    fout = open("statistics.txt", "w")
    fout.write("|    Grid size    |    # Clauses    |    # Empty cells    |     Algorithm     |    Time         |\n")
    print_header_line(fout)
    print_header_line(fout)
    # Read each output file
    for i in range(1, main.NFILE + 1):
        with open(str(f'../testcases/output_{i}.txt')) as f:
            row, mul_sign, col = [x for x in next(f).split()]
            
            nclauses, tmp = [x for x in next(f).split()]

            empty_cells, tmp1, tmp2 = [x for x in next(f).split()]

            line_t1 = 4 + int(row) + 1
            line_t2 = line_t1 + int(row) + 2 + 1
            line_t3 = line_t2 + int(row) + 2 + 1

            time_1 = None
            time_2 = None
            time_3 = None

            if int(row) > 6 and int(col) > 6:
                line_t3 = -1

            cnt = 3
            while next(f, None):
                cnt += 1
                # print("cnt=",cnt)
                if cnt == line_t1 - 1:
                    time_1, tmp = [x for x in next(f).split()]
                    cnt += 1
                elif cnt == line_t2 - 1: 
                    time_2, tmp = [x for x in next(f).split()]
                    cnt += 1
                elif line_t3 != -1 and cnt == line_t3 - 1:
                    time_3, tmp = [x for x in next(f).split()]
                    break

            print_algo(fout, row, col, nclauses, empty_cells, time_1, "pysat")
            print_algo(fout, row, col, nclauses, empty_cells, time_2, "backtrack")
            print_algo(fout, row, col, nclauses, empty_cells, time_3, "bruteforce")
            print_header_line(fout)    

    fout.close()

show_experiments()
