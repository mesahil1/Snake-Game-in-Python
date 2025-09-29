#!/usr/bin/env python3
"""
Snake Game Web Server
Run this script with: python snake.py
Then open your browser to: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import sys
import socket
from urllib.parse import urlparse

# Embedded HTML content
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snake Game</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #2c3e50;
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .game-container {
            text-align: center;
            background-color: #34495e;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        h1 {
            color: #ecf0f1;
            margin: 0 0 20px 0;
            font-size: 2.5em;
        }

        .score-display {
            color: #f1c40f;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
        }

        #gameCanvas {
            border: 3px solid #ecf0f1;
            border-radius: 5px;
            background-color: #3299d9;
            display: block;
            margin: 0 auto;
        }

        .controls {
            margin-top: 15px;
            color: #ecf0f1;
        }

        .controls p {
            margin: 10px 0;
            font-size: 1.1em;
        }

        .game-over-message {
            background-color: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
            font-size: 1.2em;
            font-weight: bold;
        }

        .game-over-message p {
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Snake Game</h1>
        <div class="score-display">
            <span id="score">Your Score: 0</span>
        </div>
        <canvas id="gameCanvas" width="600" height="400"></canvas>
        <div class="controls">
            <p>Use arrow keys to control the snake</p>
            <div id="gameOverMessage" class="game-over-message" style="display: none;">
                <p>Game Over! Press 'R' to restart or 'Q' to quit.</p>
            </div>
        </div>
    </div>
    <script>
        // Game constants - matching the original Python version
        const CANVAS_WIDTH = 600;
        const CANVAS_HEIGHT = 400;
        const SNAKE_BLOCK = 10;
        const SNAKE_SPEED = 150; // milliseconds (converted from pygame clock.tick(15))

        // Colors - matching the original Python version
        const COLORS = {
            white: '#ffffff',
            yellow: '#ffff66', 
            black: '#000000',
            red: '#d53250',
            green: '#00ff00',
            blue: '#3299d9'
        };

        // Game state
        let gameState = {
            gameOver: false,
            gameClose: false,
            x1: CANVAS_WIDTH / 2,
            y1: CANVAS_HEIGHT / 2,
            x1Change: 0,
            y1Change: 0,
            snakeList: [],
            lengthOfSnake: 1,
            foodX: 0,
            foodY: 0,
            score: 0
        };

        // Get canvas and context
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const gameOverMessage = document.getElementById('gameOverMessage');

        // Initialize game
        function initGame() {
            gameState = {
                gameOver: false,
                gameClose: false,
                x1: CANVAS_WIDTH / 2,
                y1: CANVAS_HEIGHT / 2,
                x1Change: 0,
                y1Change: 0,
                snakeList: [],
                lengthOfSnake: 1,
                foodX: Math.floor(Math.random() * (CANVAS_WIDTH - SNAKE_BLOCK) / 10) * 10,
                foodY: Math.floor(Math.random() * (CANVAS_HEIGHT - SNAKE_BLOCK) / 10) * 10,
                score: 0
            };
            updateScore();
            gameOverMessage.style.display = 'none';
        }

        // Update score display
        function updateScore() {
            scoreElement.textContent = `Your Score: ${gameState.score}`;
        }

        // Draw rectangle helper
        function drawRect(x, y, width, height, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, width, height);
        }

        // Draw text helper
        function drawText(text, x, y, color, font = '25px Arial') {
            ctx.fillStyle = color;
            ctx.font = font;
            ctx.fillText(text, x, y);
        }

        // Draw snake
        function drawSnake() {
            for (let segment of gameState.snakeList) {
                drawRect(segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK, COLORS.red);
            }
        }

        // Generate new food position
        function generateFood() {
            gameState.foodX = Math.floor(Math.random() * (CANVAS_WIDTH - SNAKE_BLOCK) / 10) * 10;
            gameState.foodY = Math.floor(Math.random() * (CANVAS_HEIGHT - SNAKE_BLOCK) / 10) * 10;
        }

        // Check collision with self
        function checkSelfCollision() {
            const head = [gameState.x1, gameState.y1];
            for (let i = 0; i < gameState.snakeList.length - 1; i++) {
                if (gameState.snakeList[i][0] === head[0] && gameState.snakeList[i][1] === head[1]) {
                    return true;
                }
            }
            return false;
        }

        // Game loop
        function gameLoop() {
            if (gameState.gameOver) return;

            if (gameState.gameClose) {
                // Draw game over screen
                ctx.fillStyle = COLORS.blue;
                ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
                
                drawText("Game Over! Press 'R' to restart. Press 'Q' to quit.", 
                        CANVAS_WIDTH / 6, CANVAS_HEIGHT / 3, COLORS.red, '20px Arial');
                updateScore();
                gameOverMessage.style.display = 'block';
                return;
            }

            // Check boundary collisions
            if (gameState.x1 >= CANVAS_WIDTH || gameState.x1 < 0 || 
                gameState.y1 >= CANVAS_HEIGHT || gameState.y1 < 0) {
                gameState.gameClose = true;
                return;
            }

            // Update snake position
            gameState.x1 += gameState.x1Change;
            gameState.y1 += gameState.y1Change;

            // Clear canvas and draw background
            ctx.fillStyle = COLORS.blue;
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            // Draw food
            drawRect(gameState.foodX, gameState.foodY, SNAKE_BLOCK, SNAKE_BLOCK, COLORS.green);

            // Add new head to snake
            const snakeHead = [gameState.x1, gameState.y1];
            gameState.snakeList.push(snakeHead);

            // Remove tail if snake hasn't grown
            if (gameState.snakeList.length > gameState.lengthOfSnake) {
                gameState.snakeList.shift();
            }

            // Check self collision
            if (checkSelfCollision()) {
                gameState.gameClose = true;
                return;
            }

            // Draw snake
            drawSnake();

            // Update score display
            updateScore();

            // Check food collision
            if (gameState.x1 === gameState.foodX && gameState.y1 === gameState.foodY) {
                generateFood();
                gameState.lengthOfSnake += 1;
                gameState.score += 1;
            }

            // Continue game loop
            setTimeout(gameLoop, SNAKE_SPEED);
        }

        // Handle keyboard input
        document.addEventListener('keydown', function(event) {
            if (gameState.gameClose) {
                if (event.key.toLowerCase() === 'r' || event.key.toLowerCase() === 'c') {
                    initGame();
                    gameLoop();
                } else if (event.key.toLowerCase() === 'q') {
                    gameState.gameOver = true;
                    alert('Thanks for playing!');
                }
                return;
            }

            switch(event.key) {
                case 'ArrowLeft':
                    gameState.x1Change = -SNAKE_BLOCK;
                    gameState.y1Change = 0;
                    break;
                case 'ArrowRight':
                    gameState.x1Change = SNAKE_BLOCK;
                    gameState.y1Change = 0;
                    break;
                case 'ArrowUp':
                    gameState.y1Change = -SNAKE_BLOCK;
                    gameState.x1Change = 0;
                    break;
                case 'ArrowDown':
                    gameState.y1Change = SNAKE_BLOCK;
                    gameState.x1Change = 0;
                    break;
            }
        });

        // Start the game
        initGame();
        gameLoop();
    </script>
</body>
</html>'''


class SnakeGameHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for serving the Snake Game"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            # Serve the embedded HTML content
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            # For any other path, return 404
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Not Found</h1><p>Go to <a href="/">Snake Game</a></p>')
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[Server] {format % args}")


def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None


def open_browser(port):
    """Open the default browser to the game URL after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open(f'http://localhost:{port}')


def main():
    """Main function to start the Snake Game web server"""
    print("🐍 Starting Snake Game Web Server...")
    
    # Find an available port
    port = find_free_port()
    if port is None:
        print("❌ Error: Could not find an available port.")
        print("💡 Try closing other applications and try again.")
        sys.exit(1)
    
    print(f"Server will run on: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Create and configure the server
        with socketserver.TCPServer(("", port), SnakeGameHandler) as httpd:
            print(f"✅ Server started successfully on port {port}")
            print("🌐 Opening game in your default browser...")
            
            # Start browser in a separate thread
            browser_thread = threading.Thread(target=open_browser, args=(port,))
            browser_thread.daemon = True
            browser_thread.start()
            
            print("🎮 Enjoy playing Snake! Use arrow keys to control.")
            print(f"💡 Tip: You can also manually open http://localhost:{port} in any browser")
            print()
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for playing Snake!")
        sys.exit(0)
    except OSError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 