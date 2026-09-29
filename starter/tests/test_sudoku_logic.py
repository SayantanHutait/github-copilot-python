import sudoku_logic


def test_create_empty_board_is_9x9_with_zeroes():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_returns_independent_board():
    board = sudoku_logic.create_empty_board()
    copied = sudoku_logic.deep_copy(board)

    copied[0][0] = 9

    assert board[0][0] == sudoku_logic.EMPTY
    assert copied[0][0] == 9


def test_is_safe_rejects_existing_row_column_or_box_values():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5
    board[3][0] = 6
    board[1][1] = 7

    assert sudoku_logic.is_safe(board, 0, 0, 5) is False
    assert sudoku_logic.is_safe(board, 0, 0, 6) is False
    assert sudoku_logic.is_safe(board, 0, 0, 7) is False


def test_is_safe_allows_valid_candidate():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5
    board[3][0] = 6
    board[1][1] = 7

    assert sudoku_logic.is_safe(board, 0, 0, 4) is True


def test_fill_board_generates_valid_completed_grid():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True

    expected = set(range(1, sudoku_logic.SIZE + 1))
    for row in board:
        assert set(row) == expected

    for col in range(sudoku_logic.SIZE):
        assert {board[row][col] for row in range(sudoku_logic.SIZE)} == expected


def test_generate_puzzle_default_returns_puzzle_and_solution_shapes():
    puzzle, solution = sudoku_logic.generate_puzzle()

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert sum(cell == sudoku_logic.EMPTY for row in puzzle for cell in row) == (
        sudoku_logic.SIZE * sudoku_logic.SIZE - 35
    )


def test_generate_puzzle_with_more_than_81_clues_keeps_full_board():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=100)

    assert sum(cell == sudoku_logic.EMPTY for row in puzzle for cell in row) == 0


def test_count_solutions_returns_one_for_completed_valid_board():
    _, solution = sudoku_logic.generate_puzzle(clues=81)

    assert sudoku_logic.count_solutions(solution) == 1


def test_count_solutions_detects_multiple_solutions():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 3, 5, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 0, 0],
        [0, 0, 1, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    assert sudoku_logic.count_solutions(board, limit=2) == 2


def test_generate_puzzle_produces_uniquely_solvable_puzzle():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle, limit=2) == 1
