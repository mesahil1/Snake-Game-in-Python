// Game constants - matching the Python version
const CANVAS_WIDTH = 600;
const CANVAS_HEIGHT = 400;
const SNAKE_BLOCK = 10;
const SNAKE_SPEED = 150; // milliseconds (converted from pygame clock.tick(15))

// Colors - matching the Python version
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