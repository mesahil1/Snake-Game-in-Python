# Snake Game in Python

A browser-based Snake game that runs from a single Python file without any external dependencies.

## How to Run

Simply run the Python script to start the web server:

```bash
python3 snake.py
```

This will:
- Start a local web server on port 8000
- Automatically open the game in your default browser
- Serve the Snake game at `http://localhost:8000`

No installation of external libraries is required! The game uses only Python's built-in modules.

## How to Play

- **Arrow Keys**: Control the snake's movement
- **Objective**: Eat the green food to grow and increase your score
- **Avoid**: Hitting the walls or the snake's own body
- **Game Over**: Press 'R' to restart or 'Q' to quit

## Features

- **Self-contained**: Everything embedded in a single Python file
- **No dependencies**: Uses only Python standard library
- **Browser-based**: Runs in any modern web browser
- **Responsive**: Clean, responsive design
- **Faithful gameplay**: Maintains the classic Snake game mechanics

## Technical Details

The game is implemented as:
- A Python HTTP server using `http.server` and `socketserver`
- HTML5 Canvas for rendering
- JavaScript for game logic and user input
- CSS for styling
- All content embedded directly in the Python file

Press `Ctrl+C` in the terminal to stop the server when done playing.

