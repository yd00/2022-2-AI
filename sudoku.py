import math

ROWS_NUM = COLS_NUM = 9
puzzle = [[0 for col in range(COLS_NUM)] for row in range(ROWS_NUM)]
peers = dict()


def input_puzzle():
    print(f'Enter the sudoku puzzle in a row-major fashion')
    for row in range(ROWS_NUM):
        numbers = input(f'\trow {row+1}: ')
        for col in range(COLS_NUM):
            puzzle[row] = numbers.strip().split(" ")
            puzzle[row] = [int(i) for i in puzzle[row]]


def display_puzzle(puzzle):
    for row in range(ROWS_NUM):
        output = ''
        for col in range(COLS_NUM):
            output += f'{puzzle[row][col]}   '
        print(output)


def define_peers():
    for row in range(ROWS_NUM):
        for col in range(COLS_NUM):
            selected_cells = []
            # define peers on same row for a tile
            for c in range(COLS_NUM):
                if c != col:
                    selected_cells.append(puzzle[row][c])

            # define peers on same column for a tile
            for r in range(ROWS_NUM):
                if r != row:
                    selected_cells.append(puzzle[r][col])

            # define peers in same square for a tile
            last_row_index = math.ceil((row + 1) / 3)
            for r in range(3 * last_row_index - 1, 3 * (last_row_index - 1) - 1, -1):
                if r != row:
                    last_col_index = math.ceil((col + 1) / 3)
                    for c in range(3 * last_col_index - 1, 3 * (last_col_index - 1) - 1, -1):
                        if c != col:
                            selected_cells.append(puzzle[r][c])

            peers.update({f'{row},{col}': selected_cells})


def is_valid_value(puzzle, row, col, val):
    for c in range(COLS_NUM):
        if puzzle[row][c] == val:
            return False

    for r in range(ROWS_NUM):
        if puzzle[r][col] == val:
            return False

    last_row_index = math.ceil((row + 1) / 3)
    for r in range(3 * last_row_index - 1, 3 * (last_row_index - 1) - 1, -1):
        if r != row:
            last_col_index = math.ceil((col + 1) / 3)
            for c in range(3 * last_col_index - 1, 3 * (last_col_index - 1) - 1, -1):
                if c != col:
                    if puzzle[r][c] == val:
                        return False
    return True


def solve_puzzle(puzzle):
    for row in range(ROWS_NUM):
        for col in range(COLS_NUM):
            if puzzle[row][col] == 0:
                domain = list(set(range(1, 10)) - set(peers.get(f'{row},{col}')))
                for val in domain:
                    if is_valid_value(puzzle, row, col, val):
                        puzzle[row][col] = val
                        solve_puzzle(puzzle)
                        puzzle[row][col] = 0
                return
    display_puzzle(puzzle)


input_puzzle()
define_peers()
solve_puzzle(puzzle)