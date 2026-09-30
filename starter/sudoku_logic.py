import copy
import random

SIZE = 9
EMPTY = 0


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def _find_empty(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def count_solutions(board, limit=2):
    cell = _find_empty(board)
    if cell is None:
        return 1

    row, col = cell
    total = 0
    for candidate in range(1, SIZE + 1):
        if is_safe(board, row, col, candidate):
            board[row][col] = candidate
            total += count_solutions(board, limit)
            board[row][col] = EMPTY
            if total >= limit:
                return total
    return total


def _remove_cells_with_uniqueness(board, clues):
    target_removals = SIZE * SIZE - clues
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    removed = 0
    for row, col in positions:
        if removed >= target_removals:
            break
        backup = board[row][col]
        board[row][col] = EMPTY
        board_copy = deep_copy(board)
        if count_solutions(board_copy) == 1:
            removed += 1
        else:
            board[row][col] = backup

    return removed == target_removals


def generate_puzzle(clues=35):
    clues = max(17, min(80, int(clues)))

    for _ in range(20):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)

        puzzle = deep_copy(board)
        if _remove_cells_with_uniqueness(puzzle, clues):
            return puzzle, solution

    raise RuntimeError('Unable to generate a unique puzzle with requested clues')
