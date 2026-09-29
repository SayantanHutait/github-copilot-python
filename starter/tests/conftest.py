from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app as sudoku_app


@pytest.fixture(autouse=True)
def reset_current_game_state():
    sudoku_app.CURRENT['puzzle'] = None
    sudoku_app.CURRENT['solution'] = None
    yield
    sudoku_app.CURRENT['puzzle'] = None
    sudoku_app.CURRENT['solution'] = None


@pytest.fixture
def client():
    with sudoku_app.app.test_client() as client:
        yield client
