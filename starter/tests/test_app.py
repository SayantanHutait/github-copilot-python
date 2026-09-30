import app


def test_new_game_respects_difficulty_mapping():
    client = app.app.test_client()

    easy = client.get('/new?difficulty=easy').get_json()
    assert easy['difficulty'] == 'easy'
    assert easy['clues'] == 40
    assert sum(1 for row in easy['puzzle'] for value in row if value != 0) == 40

    unknown = client.get('/new?difficulty=unknown').get_json()
    assert unknown['difficulty'] == 'medium'
    assert unknown['clues'] == 35


def test_hint_and_check_require_current_game_id():
    client = app.app.test_client()

    payload = client.get('/new?difficulty=hard').get_json()
    game_id = payload['gameId']

    hint = client.get(f'/hint?gameId={game_id}')
    assert hint.status_code == 200
    assert {'row', 'col', 'value'} <= set(hint.get_json())

    stale = client.post('/check', json={'board': payload['puzzle'], 'gameId': 'wrong-id'})
    assert stale.status_code == 400


def test_check_validates_board_shape():
    client = app.app.test_client()
    payload = client.get('/new').get_json()

    bad = client.post('/check', json={'board': [[0]], 'gameId': payload['gameId']})
    assert bad.status_code == 400
    assert bad.get_json()['error'] == 'Invalid board data'
