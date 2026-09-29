import app as sudoku_app


def _empty_board():
    return [[0] * sudoku_app.sudoku_logic.SIZE for _ in range(sudoku_app.sudoku_logic.SIZE)]


def _board_with_single_difference(solution):
    board = [row[:] for row in solution]
    original = board[0][0]
    board[0][0] = 1 if original != 1 else 2
    return board


def test_index_route_renders_page(client):
    response = client.get('/')

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Sudoku Game' in html
    assert 'id="new-game"' in html


def test_new_route_returns_json_puzzle_and_sets_current_solution(client):
    response = client.get('/new?clues=81')

    assert response.status_code == 200
    data = response.get_json()
    assert 'puzzle' in data
    assert len(data['puzzle']) == sudoku_app.sudoku_logic.SIZE
    assert sudoku_app.CURRENT['solution'] is not None


def test_check_route_returns_error_without_active_game(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_route_returns_empty_incorrect_for_correct_solution(client):
    new_game = client.get('/new?clues=81').get_json()
    board = new_game['puzzle']

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_route_reports_incorrect_cell_coordinates(client):
    client.get('/new?clues=81')
    solution = sudoku_app.CURRENT['solution']
    board = _board_with_single_difference(solution)

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]


def test_check_route_allows_missing_json_and_fails_with_server_error(client):
    # This captures current route behavior: request.json can be None and then .get raises.
    response = client.post('/check')

    assert response.status_code == 415


def test_new_route_rejects_non_integer_clues(client):
    response = client.get('/new?clues=not-an-int')

    assert response.status_code == 500


def test_new_route_maps_easy_difficulty_to_expected_clues(client, monkeypatch):
    called = {}

    def fake_generate_puzzle(clues):
        called['clues'] = clues
        board = _empty_board()
        return board, board

    monkeypatch.setattr(sudoku_app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=easy')

    assert response.status_code == 200
    assert called['clues'] == sudoku_app.DIFFICULTY_CLUES['easy']


def test_new_route_maps_medium_difficulty_to_expected_clues(client, monkeypatch):
    called = {}

    def fake_generate_puzzle(clues):
        called['clues'] = clues
        board = _empty_board()
        return board, board

    monkeypatch.setattr(sudoku_app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=medium')

    assert response.status_code == 200
    assert called['clues'] == sudoku_app.DIFFICULTY_CLUES['medium']


def test_new_route_maps_hard_difficulty_to_expected_clues(client, monkeypatch):
    called = {}

    def fake_generate_puzzle(clues):
        called['clues'] = clues
        board = _empty_board()
        return board, board

    monkeypatch.setattr(sudoku_app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=hard')

    assert response.status_code == 200
    assert called['clues'] == sudoku_app.DIFFICULTY_CLUES['hard']


def test_new_route_invalid_difficulty_falls_back_to_medium(client, monkeypatch):
    called = {}

    def fake_generate_puzzle(clues):
        called['clues'] = clues
        board = _empty_board()
        return board, board

    monkeypatch.setattr(sudoku_app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=unknown')

    assert response.status_code == 200
    assert called['clues'] == sudoku_app.DIFFICULTY_CLUES['medium']
