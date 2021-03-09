#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import copy
import time
import statistics
from statistics import mean

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def backtracking(board):
    """Takes a board and returns solved board."""

    # initialize domain for empty spaces (value == 0) on the 9x9 grid
    # initial domain values for all variables is a list of 1-9
    domain = {}
    for i in ROW:
        for j in COL:
            if board[i+j] == 0:
                domain[i+j] = list(range(1,10))
                #print(i+j,domain[i+j])

    # preprocessing - perform AC3 (arc consistency check) on all variables in the domain
    # establish constraints
    for key in domain.keys():
        if arc_consistent(key[0], key[1], board, domain) == False:
            return False
        # if any variable has no legal values left in its domain, the soduku can't be solved, program terminates

    # call recursive backtrack helper method here
    solved_board = backtrack_helper(board, domain)

    #solved_board = board
    return solved_board

def backtrack_helper(board, domain):
    if isComplete(board):
        return board

    #select next variable to run backtrack
    var = mrv(board, domain)
    row = var[0]
    col = var[1]
    for val in domain[var]:
        if isConsistent(val, row, col, board):
            fwd_result = forward_check(val, row, col, domain)
            if fwd_result != False:
                # when there is no empty domain in all variables in the domain
                # result is the updated domain returned by forward_check
                board[row + col] = val # make an assignment
                updated_domain = fwd_result # update domain
                # else if there is empty domain in some variables in domain, no need to update current domain
                result = backtrack_helper(board,updated_domain) # recursively call backtrack to check the next variable
                if result != False:
                    return result
                else:
                    # reverse the assignment since backtrack fails at some point down the road
                    board[row + col] = 0 
    return False

def isComplete(board):
    """ check if current board is complete, ie fully assigned with no zero in any space"""
    for value in board.values():
        if value == 0:
            return False
    return True

def isConsistent(val, row, col, board):
    """check whether one val of a variable is consistent with the remaining board"""

    # check the entire row 
    for c in range(9):
        if board[row + COL[c]] == val:
            return False

    # check the entire column
    for r in ROW:
        if board[r + col] == val:
            return False

    ## check the entire 3x3 grid
    # begin_r represent the beginning row index for one of nine subsections in 9x9 grid
    begin_r = list(ROW).index(row) // 3 * 3 
    # begin_c represents the beginning col. index for one of nine subsections in 9x9 grid
    begin_c = (int(col) - 1) // 3 * 3
    
    for i in range(3):
        for j in range(3):
            if board[ROW[begin_r + i] + COL[begin_c + j]] == val:
                return False
    return True

def arc_consistent(row, col, board, domain):
    """for each variable in 9x9 grid, eliminate values from domain which is not consistent to reduce domain size"""
    """ arc consistency check for a single variable and update its domain"""

    # reduce domain of a variable by removing items already appeared in the same row
    for c in range(9):
        if board[row + COL[c]] in domain[row + col]:
            domain[row + col].remove(board[row + COL[c]])
            if not domain[row + col]:
                return False
                # when domain becomes empty

    # reduce domain of a variable by removing items already appeared in the same column
    for r in ROW:
        if board[r + col] in domain[row + col]:
            domain[row + col].remove(board[r + col])
            if not domain[row + col]:
                return False
                # when domain becomes empty

    # begin_r represent the beginning row index for one of nine subsections in 9x9 grid
    begin_r = list(ROW).index(row) // 3 * 3 
    # begin_c represents the beginning col. index for one of nine subsections in 9x9 grid
    begin_c = (int(col) - 1) // 3 * 3
    
    for i in range(3):
        for j in range(3):
            if board[ROW[begin_r + i] + COL[begin_c + j]] in domain[row + col]:
                domain[row + col].remove(board[ROW[begin_r + i] + COL[begin_c + j]])
                if not domain[row + col]:
                    return False
                    # when domain becomes empty
    return True

def forward_check(val, row, col, domain):
    """ after value val is assigned to variable domain[row+col], need to check all other variables having constraints """
    """ with the assigned variable and update their domain by reducing val from it"""
    """ return False if any variables are left with zero legal values, original domain unchanged; otherwise, return the revised domain """

    updated_domain = copy.deepcopy(domain)

    # go thru all other variables in the same row
    for c in range(9):
        if COL[c] != col and row + COL[c] in updated_domain.keys():
            val_list = updated_domain[row + COL[c]]
            if val in val_list:
                val_list.remove(val)
                if not val_list:
                    return False
                    # it is illegal once domain of a variable becomes empty

    # go thru all other variables in the same column
    for r in ROW:
        if r != row and r + col in updated_domain.keys():
            val_list = updated_domain[r + col]
            if val in val_list:
                val_list.remove(val)
                if not val_list:
                    return False
                    # it is illegal once domain of a variable becomes empty

    # begin_r represent the beginning row index for one of nine subsections in 9x9 grid
    begin_r = list(ROW).index(row) // 3 * 3 
    # begin_c represents the beginning col. index for one of nine subsections in 9x9 grid
    begin_c = (int(col) - 1) // 3 * 3
    
    for i in range(3):
        for j in range(3):
            if ROW[begin_r + i] != row and COL[begin_c + j] != col and ROW[begin_r + i] + COL[begin_c + j] in updated_domain.keys():
                val_list = updated_domain[ROW[begin_r + i] + COL[begin_c + j]]
                if val in val_list:
                    val_list.remove(val)
                    if not val_list:
                        return False
                        # it is illegal once domain of a variable becomes empty
    return updated_domain

def mrv(board, domain):
    """ Minimum remaining variables heuristics to pick the next variable for backtracking """
    var=''
    num_values = 10
    for key, value in domain.items():
        if len(value) < num_values and board[key] == 0:
            # must select from unassigned variables
            var = key
            num_values = len(value)
    return var             

if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # a list to store running time for each board
    runtime_stat = []

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue
        # starting time to run a new board
        start_time  = time.time()
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        # Print starting board.
        # print_board(board)

        # Solve with backtracking
        solved_board = backtracking(board)
        # finishing time after solving a board
        end_time = time.time()
        runtime_stat.append(end_time - start_time)
        # Print solved board.
        # print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    print("Finishing all boards in file.")
    # print("Mininum runtime: %.8f"%min(runtime_stat))
    # print("Maxinum runtime: %.8f"%max(runtime_stat))
    # print("Mean runtime: %.8f"%mean(runtime_stat))
    # print("Runtime standard deviation: %.8f"%statistics.stdev(runtime_stat))
    # print("Total runtime: %.8f"%sum(runtime_stat))
    # print("running_time: %.8f"%(end_time - start_time))