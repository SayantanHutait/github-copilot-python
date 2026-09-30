from uuid import uuid4

from flask import Flask, jsonify, render_template, request

import sudoku_logic

app = Flask(__name__)

DIFFICULTY_CLUES = {
    'easy': 40,
    'medium': 35,
    'hard': 30,
}

CURRENT = {
    'puzzle': None,
    'solution': None,
    'difficulty': 'medium',
    'game_id': None,
}


@app.route('/')
def index():
    return render_template('index.html')


def _resolve_difficulty_and_clues(args):
    difficulty = (args.get('difficulty') or 'medium').lower()

    if 'clues' in args:
        try:
            clues = int(args.get('clues'))
        except (TypeError, ValueError):
            clues = DIFFICULTY_CLUES['medium']
    else:
        clues = DIFFICULTY_CLUES.get(difficulty, DIFFICULTY_CLUES['medium'])

    clues = max(17, min(80, clues))
    if difficulty not in DIFFICULTY_CLUES:
        difficulty = 'medium'

    return difficulty, clues


def _is_current_game(game_id):
    return not game_id or game_id == CURRENT.get('game_id')


@app.route('/new')
def new_game():
    difficulty, clues = _resolve_difficulty_and_clues(request.args)

    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['difficulty'] = difficulty
    CURRENT['game_id'] = str(uuid4())

    return jsonify(
        {
            'puzzle': puzzle,
            'difficulty': difficulty,
            'clues': clues,
            'gameId': CURRENT['game_id'],
        }
    )


@app.route('/hint')
def hint():
    if CURRENT.get('solution') is None:
        return jsonify({'error': 'No game in progress'}), 400

    game_id = request.args.get('gameId')
    if not _is_current_game(game_id):
        return jsonify({'error': 'Game is no longer active. Start a new game.'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if CURRENT['puzzle'][row][col] == sudoku_logic.EMPTY:
                value = CURRENT['solution'][row][col]
                CURRENT['puzzle'][row][col] = value
                return jsonify({'row': row, 'col': col, 'value': value})

    return jsonify({'error': 'No empty cells available for hints'}), 400


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json or {}
    board = data.get('board')
    solution = CURRENT.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    if not _is_current_game(data.get('gameId')):
        return jsonify({'error': 'Game is no longer active. Start a new game.'}), 400

    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Invalid board data'}), 400

    for row in board:
        if not isinstance(row, list) or len(row) != sudoku_logic.SIZE:
            return jsonify({'error': 'Invalid board data'}), 400

    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])

    complete = len(incorrect) == 0
    return jsonify({'incorrect': incorrect, 'complete': complete})


if __name__ == '__main__':
    app.run(debug=True)
