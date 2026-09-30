import random

import sudoku_logic


def test_generate_puzzle_has_unique_solution_and_requested_clues():
    random.seed(42)
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    clue_count = sum(1 for row in puzzle for value in row if value != sudoku_logic.EMPTY)
    assert clue_count == 35

    solution_count = sudoku_logic.count_solutions(sudoku_logic.deep_copy(puzzle))
    assert solution_count == 1

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] != sudoku_logic.EMPTY:
                assert puzzle[row][col] == solution[row][col]
