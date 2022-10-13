from copy import deepcopy
from itertools import combinations
import numpy as np

clues_row = dict()
clues_col = dict()
selected_clues = dict()
combinations_row = dict()
combinations_col = dict()
board = []

print("***WELCOME TO YAW'S NONOGRAM SOLVER***\n")
rows_num = int(input('Enter the number of rows: '))
cols_num = int(input('Enter the number of columns: '))
board = np.zeros((rows_num, cols_num), dtype=int)

print('\nEnter the clues for each row as a space-separated list of numbers:')
for row in range(rows_num):
    val = input(f'\trow {row + 1}: ')
    clues_row[str(row)] = [int(i) for i in val.strip().split(" ")]

print('\nEnter the clues for each column as a space-separated list of numbers:')
for col in range(cols_num):
    val = input(f'\tcol {col + 1}: ')
    clues_col[str(col)] = [int(i) for i in val.strip().split(" ")]


def display_board():
    for row in range(rows_num):
        output = ''
        for col in range(cols_num):
            output += f'{"*   " if board[row][col]==1 else "    "}'
        print(f'\n{output}')


def is_valid_combination(row_combination, index):
    temp = deepcopy(board[index])
    board[index] = row_combination

    for row in range(rows_num):
        if sum(board[row]) > sum(clues_row[str(row)]):
            board[index] = temp
            return False

    for col in range(cols_num):
        if sum(board[:, col]) > sum(clues_col[str(col)]):
            board[index] = temp
            return False

    board[index] = temp
    return True


def create_combinations(clues_dict, length_of_dimension, dimension): # length_of_dimension = length of row/column
    for key, clues in clues_dict.items():
        valid_combinations = []
        clues_num = len(clues)
        no_empty = length_of_dimension - clues_num - sum(clues) + 1
        ones = [[1] * x for x in clues]

        for c in combinations(range(clues_num + no_empty), clues_num):
            selected = [-1] * (clues_num + no_empty)
            filled_indices = 0
            for val in c:
                selected[val] = filled_indices
                filled_indices += 1
            res_opt = [ones[val] + [-1] if val > -1 else [-1] for val in selected]
            res_opt = [item for sublist in res_opt for item in sublist][:-1]
            valid_combinations.append(res_opt)
        if dimension:
            combinations_row[key] = valid_combinations
        else:
            combinations_col[key] = valid_combinations


def create_row_combinations():
    create_combinations(clues_row, cols_num, True)


def create_col_combinations():
    create_combinations(clues_col, rows_num, False)


def solve():
    for row, row_combinations in sorted(combinations_row.items(), key=lambda k: len(k[1])):  # start with those with fewer combinations
        if sum(board[int(row)]) < sum(clues_row[row]):
            for row_combination in row_combinations:
                row_combination = [0 if rc == -1 else 1 for rc in row_combination]
                if is_valid_combination(row_combination, int(row)):
                    row_temp = deepcopy(board[int(row)])
                    board[int(row)] = row_combination
                    solve()
                    board[int(row)] = row_temp
            return

    for col in range(cols_num):
        arr = [-1 if x == 0 else 1 for x in board[:, col]]
        if arr not in combinations_col[str(col)]:
            return
    display_board()


create_row_combinations()
create_col_combinations()
solve()