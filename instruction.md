# Sudoku Project Instructions

## Project Overview

This is a Flask-based Sudoku web application using:
- Python
- Flask
- HTML
- CSS
- Vanilla JavaScript

The application should remain simple, modular, readable, and maintainable.

## Project Structure

- `starter/app.py` — Flask routes and backend application logic
- `starter/sudoku_logic.py` — Sudoku generation, solving, and validation
- `starter/templates/` — HTML templates
- `starter/static/main.js` — frontend JavaScript
- `starter/static/styles.css` — application styling
- `starter/tests/` — pytest tests
- `Screenshots/` — Copilot milestone screenshots

## Coding Guidelines

- Prefer small, reusable functions.
- Keep backend, Sudoku logic, and frontend responsibilities separated.
- Do not modify unrelated functionality when implementing a feature.
- Preserve existing APIs unless there is a clear reason to change them.
- Use clear variable and function names.
- Add comments only where they improve understanding.
- Handle invalid input gracefully.
- Avoid unnecessary dependencies.

## Sudoku Requirements

- Every generated puzzle must have exactly one solution.
- Support Easy, Medium, and Hard difficulty levels.
- Difficulty levels must change the number of prefilled cells.
- Prefilled cells must not be editable.
- User entries should be validated.
- Invalid entries should receive immediate visual feedback.
- A completed correct puzzle should display a completion message.

## Frontend Requirements

- Use semantic HTML where appropriate.
- Keep the interface responsive on desktop and mobile.
- The Sudoku 3x3 blocks should have alternating visual styling.
- Controls should remain readable and usable on small screens.
- Support both light and dark modes.
- Maintain readable contrast and accessible controls.

## Game Features

The application should support:

- Difficulty selection
- Hint button
- Check button
- Timer
- Completion message
- Top 10 fastest scores
- Local storage persistence
- Dark mode

## Testing

- Use pytest for backend and Sudoku logic tests.
- Run the existing tests before changing functionality.
- Run the complete test suite after implementing a feature.
- New functionality should have appropriate tests where practical.
- Do not remove or weaken existing tests simply to make them pass.

## GitHub Copilot Usage

Before implementing a major feature:
1. Inspect the existing code.
2. Explain the intended changes.
3. Make focused changes.
4. Review Copilot's generated code.
5. Reject or modify suggestions that do not satisfy the project requirements.
6. Run the tests after changes.

Do not blindly accept generated code.

## Scope Control

Implement features incrementally.

Do not introduce unrelated frameworks, dependencies, or architectural changes unless they are necessary for the project requirements.
