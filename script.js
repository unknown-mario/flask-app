// Game elements
const playerPaddle = document.getElementById('player-paddle');
const computerPaddle = document.getElementById('computer-paddle');
const ball = document.getElementById('ball');
const playerScoreDisplay = document.getElementById('player-score');
const computerScoreDisplay = document.getElementById('computer-score');
const startButton = document.getElementById('start-button');
const gameBoard = document.getElementById('game-board');

// Game state
let gameInterval;
let ballSpeedX = 5;
let ballSpeedY = 3;
let playerScore = 0;
let computerScore = 0;
let gameRunning = false;

// Initial paddle positions
let playerPaddleY = 150;
let computerPaddleY = 150;
let ballX = 300;
let ballY = 195;

// Computer difficulty (1-10, higher = more difficult)
const computerDifficulty = 5;

// Initialize game
function initGame() {
    // Reset positions
    playerPaddleY = 150;
    computerPaddleY = 150;
    ballX = 300;
    ballY = 195;
    
    // Reset display
    playerPaddle.style.top = playerPaddleY + 'px';
    computerPaddle.style.top = computerPaddleY + 'px';
    ball.style.left = ballX + 'px';
    ball.style.top = ballY + 'px';
    
    // Reset scores if needed
    if (!gameRunning) {
        playerScore = 0;
        computerScore = 0;
        playerScoreDisplay.textContent = '0';
        computerScoreDisplay.textContent = '0';
    }
}

// Start the game
function startGame() {
    if (gameRunning) return;
    
    initGame();
    gameRunning = true;
    startButton.textContent = 'Restart Game';
    
    // Start game loop
    gameInterval = setInterval(updateGame, 16); // ~60fps
}

// Update game state
function updateGame() {
    // Move the ball
    ballX += ballSpeedX;
    ballY += ballSpeedY;
    
    // Ball collision with top and bottom walls
    if (ballY <= 0 || ballY >= 385) {
        ballSpeedY = -ballSpeedY;
    }
    
    // Ball collision with paddles
    if (
        ballX <= 30 && 
        ballY + 15 >= playerPaddleY && 
        ballY <= playerPaddleY + 100
    ) {
        ballSpeedX = -ballSpeedX;
        // Add some randomness to the bounce
        adjustBallSpeed();
    }
    
    if (
        ballX >= 560 && 
        ballY + 15 >= computerPaddleY && 
        ballY <= computerPaddleY + 100
    ) {
        ballSpeedX = -ballSpeedX;
        // Add some randomness to the bounce
        adjustBallSpeed();
    }
    
    // Ball out of bounds - scoring
    if (ballX < 0) {
        // Computer scores
        computerScore++;
        computerScoreDisplay.textContent = computerScore;
        resetBall();
    } else if (ballX > 600) {
        // Player scores
        playerScore++;
        playerScoreDisplay.textContent = playerScore;
        resetBall();
    }
    
    // Move computer paddle
    moveComputerPaddle();
    
    // Update positions
    ball.style.left = ballX + 'px';
    ball.style.top = ballY + 'px';
    playerPaddle.style.top = playerPaddleY + 'px';
    computerPaddle.style.top = computerPaddleY + 'px';
}

// Reset ball after scoring
function resetBall() {
    ballX = 300;
    ballY = 195;
    // Randomize direction after reset
    ballSpeedX = Math.random() > 0.5 ? 5 : -5;
    ballSpeedY = Math.random() > 0.5 ? 3 : -3;
}

// Adjust ball speed slightly for more interesting gameplay
function adjustBallSpeed() {
    // Slightly increase speed with each hit
    if (Math.abs(ballSpeedX) < 15) {
        ballSpeedX *= 1.05;
    }
    
    // Add some random Y variation
    ballSpeedY += (Math.random() - 0.5) * 2;
    
    // Keep Y speed reasonable
    if (Math.abs(ballSpeedY) > 8) {
        ballSpeedY = (ballSpeedY > 0) ? 8 : -8;
    }
}

// Computer AI to move paddle
function moveComputerPaddle() {
    // Follow the ball with some delay based on difficulty
    const targetY = ballY - 50;
    const distanceToMove = targetY - computerPaddleY;
    
    // Move the computer paddle toward the ball
    // The lower the difficulty, the slower it responds
    computerPaddleY += distanceToMove / (11 - computerDifficulty);
    
    // Keep paddle within bounds
    if (computerPaddleY < 0) computerPaddleY = 0;
    if (computerPaddleY > 300) computerPaddleY = 300;
}

// Handle player paddle movement with mouse
gameBoard.addEventListener('mousemove', (e) => {
    if (!gameRunning) return;
    
    // Get mouse position relative to the game board
    const gameBoardRect = gameBoard.getBoundingClientRect();
    const mouseY = e.clientY - gameBoardRect.top;
    
    // Move paddle based on mouse position
    playerPaddleY = mouseY - 50; // Center paddle on mouse
    
    // Keep paddle within bounds
    if (playerPaddleY < 0) playerPaddleY = 0;
    if (playerPaddleY > 300) playerPaddleY = 300;
});

// Handle player paddle movement with touch
gameBoard.addEventListener('touchmove', (e) => {
    if (!gameRunning) return;
    
    // Prevent scrolling when touching the game
    e.preventDefault();
    
    // Get touch position relative to the game board
    const gameBoardRect = gameBoard.getBoundingClientRect();
    const touchY = e.touches[0].clientY - gameBoardRect.top;
    
    // Move paddle based on touch position
    playerPaddleY = touchY - 50; // Center paddle on touch
    
    // Keep paddle within bounds
    if (playerPaddleY < 0) playerPaddleY = 0;
    if (playerPaddleY > 300) playerPaddleY = 300;
}, { passive: false });

// Start/restart game on button click
startButton.addEventListener('click', startGame);

// Initialize the game board
initGame();