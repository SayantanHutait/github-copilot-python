const SIZE = 9;
const GAME_STORAGE_KEY = 'sudokuCurrentGame';
const SCORES_STORAGE_KEY = 'sudokuTopScores';
const DARK_MODE_STORAGE_KEY = 'sudokuDarkMode';

const state = {
  puzzle: [],
  gameId: null,
  difficulty: 'medium',
  hintsUsed: 0,
  startTime: null,
  timerInterval: null,
  solved: false,
};

function formatTime(totalSeconds) {
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
  const seconds = String(totalSeconds % 60).padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function getElapsedSeconds() {
  if (!state.startTime) return 0;
  return Math.floor((Date.now() - state.startTime) / 1000);
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText = `Time: ${formatTime(getElapsedSeconds())}`;
}

function startTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
  }
  state.timerInterval = setInterval(() => {
    updateTimerDisplay();
    saveCurrentGame();
  }, 1000);
}

function stopTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
  }
}

function setMessage(text, type = 'error') {
  const msg = document.getElementById('message');
  msg.innerText = text;
  msg.className = type;
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';

  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.dataset.blockParity = (Math.floor(i / 3) + Math.floor(j / 3)) % 2;
      input.addEventListener('input', handleCellInput);
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, boardValues = null) {
  state.puzzle = puz;
  createBoardElement();
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');

  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const puzzleVal = puz[i][j];
      const inp = inputs[idx];
      inp.className = 'sudoku-cell';
      if (inp.dataset.blockParity === '1') {
        inp.classList.add('block-alt');
      }

      if (puzzleVal !== 0) {
        inp.value = puzzleVal;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        const restored = boardValues ? boardValues[i][j] : 0;
        inp.value = restored ? String(restored) : '';
        inp.disabled = false;
      }
    }
  }

  validateAllEditableCells();
}

function readBoardFromInputs() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const value = inputs[idx].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function markCellValidity(input, isValid) {
  input.classList.toggle('invalid-entry', !isValid);
}

function isValueValidAt(board, row, col, value) {
  if (!value) return true;

  for (let i = 0; i < SIZE; i++) {
    if (i !== col && board[row][i] === value) return false;
    if (i !== row && board[i][col] === value) return false;
  }

  const startRow = Math.floor(row / 3) * 3;
  const startCol = Math.floor(col / 3) * 3;
  for (let r = startRow; r < startRow + 3; r++) {
    for (let c = startCol; c < startCol + 3; c++) {
      if ((r !== row || c !== col) && board[r][c] === value) return false;
    }
  }

  return true;
}

function validateEditableCell(input, board = null) {
  const currentBoard = board || readBoardFromInputs();
  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const value = currentBoard[row][col];
  const valid = isValueValidAt(currentBoard, row, col, value);
  markCellValidity(input, valid);
  return valid;
}

function validateAllEditableCells() {
  const board = readBoardFromInputs();
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  let allValid = true;

  for (const input of inputs) {
    if (!input.disabled) {
      const valid = validateEditableCell(input, board);
      if (!valid) {
        allValid = false;
      }
    }
  }

  return allValid;
}

function handleCellInput(e) {
  const clean = e.target.value.replace(/[^1-9]/g, '');
  e.target.value = clean;
  validateAllEditableCells();
  saveCurrentGame();
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();

  state.difficulty = data.difficulty;
  state.gameId = data.gameId;
  state.hintsUsed = 0;
  state.startTime = Date.now();
  state.solved = false;

  document.getElementById('difficulty').value = state.difficulty;
  document.getElementById('hints-used').innerText = `Hints used: ${state.hintsUsed}`;
  setMessage('', 'neutral');
  renderPuzzle(data.puzzle);
  updateTimerDisplay();
  startTimer();
  saveCurrentGame();
}

async function requestHint() {
  if (state.solved) return;

  const res = await fetch(`/hint?gameId=${encodeURIComponent(state.gameId || '')}`);
  const data = await res.json();

  if (data.error) {
    setMessage(data.error, 'error');
    return;
  }

  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const idx = data.row * SIZE + data.col;
  const input = inputs[idx];
  input.value = String(data.value);
  input.disabled = true;
  input.classList.add('prefilled', 'hinted');

  state.hintsUsed += 1;
  document.getElementById('hints-used').innerText = `Hints used: ${state.hintsUsed}`;
  setMessage('Hint added.', 'neutral');
  saveCurrentGame();
}

async function checkSolution() {
  if (!validateAllEditableCells()) {
    setMessage('Please fix highlighted conflicts first.', 'error');
    return;
  }

  const board = readBoardFromInputs();
  const res = await fetch('/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ board, gameId: state.gameId }),
  });

  const data = await res.json();
  if (data.error) {
    setMessage(data.error, 'error');
    return;
  }

  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const incorrect = new Set(data.incorrect.map(([row, col]) => row * SIZE + col));

  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (!input.disabled) {
      input.classList.remove('incorrect');
      if (incorrect.has(idx)) {
        input.classList.add('incorrect');
      }
    }
  }

  if (data.complete) {
    state.solved = true;
    stopTimer();
    const elapsed = getElapsedSeconds();
    const name = prompt('Congratulations! Enter your name for the leaderboard:', 'Player') || 'Player';
    addScore(name, elapsed, state.hintsUsed, state.difficulty);
    renderScores();
    setMessage(
      `Congratulations! Solved in ${formatTime(elapsed)} with ${state.hintsUsed} hint(s).`,
      'success'
    );
    saveCurrentGame();
    return;
  }

  setMessage('Some cells are incorrect.', 'error');
  saveCurrentGame();
}

function addScore(name, seconds, hints, difficulty) {
  const scores = JSON.parse(localStorage.getItem(SCORES_STORAGE_KEY) || '[]');
  scores.push({ name, seconds, hints, difficulty });
  scores.sort((a, b) => a.seconds - b.seconds);
  localStorage.setItem(SCORES_STORAGE_KEY, JSON.stringify(scores.slice(0, 10)));
}

function renderScores() {
  const scores = JSON.parse(localStorage.getItem(SCORES_STORAGE_KEY) || '[]');
  const list = document.getElementById('top-scores');
  list.innerHTML = '';

  scores.forEach((score) => {
    const item = document.createElement('li');
    item.innerText = `${score.name} — ${formatTime(score.seconds)} — ${score.difficulty} — ${score.hints} hint(s)`;
    list.appendChild(item);
  });
}

function saveCurrentGame() {
  const payload = {
    puzzle: state.puzzle,
    board: readBoardFromInputs(),
    difficulty: state.difficulty,
    hintsUsed: state.hintsUsed,
    elapsedSeconds: getElapsedSeconds(),
    gameId: state.gameId,
    solved: state.solved,
  };
  localStorage.setItem(GAME_STORAGE_KEY, JSON.stringify(payload));
}

function restoreCurrentGame() {
  const saved = localStorage.getItem(GAME_STORAGE_KEY);
  if (!saved) {
    return false;
  }

  try {
    const data = JSON.parse(saved);
    if (!data.puzzle || !data.board || data.puzzle.length !== SIZE || data.board.length !== SIZE) {
      return false;
    }

    state.difficulty = data.difficulty || 'medium';
    state.hintsUsed = Number(data.hintsUsed) || 0;
    state.gameId = data.gameId || null;
    state.solved = Boolean(data.solved);
    state.startTime = Date.now() - ((Number(data.elapsedSeconds) || 0) * 1000);

    document.getElementById('difficulty').value = state.difficulty;
    document.getElementById('hints-used').innerText = `Hints used: ${state.hintsUsed}`;
    renderPuzzle(data.puzzle, data.board);
    updateTimerDisplay();
    if (!state.solved) {
      startTimer();
    }
    setMessage('Restored saved game.', 'neutral');
    return true;
  } catch (_err) {
    return false;
  }
}

function applyDarkMode(enabled) {
  document.body.classList.toggle('dark-mode', enabled);
  const button = document.getElementById('toggle-dark-mode');
  button.setAttribute('aria-pressed', String(enabled));
  button.innerText = enabled ? 'Light Mode' : 'Dark Mode';
  localStorage.setItem(DARK_MODE_STORAGE_KEY, JSON.stringify(enabled));
}

function initDarkMode() {
  const saved = localStorage.getItem(DARK_MODE_STORAGE_KEY);
  const enabled = saved ? JSON.parse(saved) : false;
  applyDarkMode(Boolean(enabled));
}

window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('toggle-dark-mode').addEventListener('click', () => {
    const enabled = !document.body.classList.contains('dark-mode');
    applyDarkMode(enabled);
  });

  initDarkMode();
  renderScores();

  if (!restoreCurrentGame()) {
    newGame();
  }
});
