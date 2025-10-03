// src/static/game.js
document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos da UI ---
    const startScreen = document.getElementById('start-screen');
    const difficultyScreen = document.getElementById('difficulty-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const gameCanvas = document.getElementById('gameCanvas');
    const scoreElement = document.getElementById('score');
    const finalScoreElement = document.getElementById('finalScore');
    const restartBtn = document.getElementById('restartBtn');

    // --- Botões ---
    const normalBtn = document.getElementById('normalBtn');
    const dificilBtn = document.getElementById('dificilBtn');

    // --- Configurações do Jogo ---
    const ctx = gameCanvas.getContext('2d');
    const gridSize = 20;
    let gameLoopInterval;

    // --- Lógica de Telas ---
    document.addEventListener('keydown', handleKeyPress);
    normalBtn.addEventListener('click', () => startGame('Normal'));
    dificilBtn.addEventListener('click', () => startGame('Dificil'));
    restartBtn.addEventListener('click', () => location.reload());

    function handleKeyPress(event) {
        if (startScreen.style.display !== 'none') {
            showDifficultyScreen();
            document.removeEventListener('keydown', handleKeyPress);
        }
    }

    function showDifficultyScreen() {
        startScreen.style.display = 'none';
        difficultyScreen.style.display = 'flex';
    }

    // --- LÓGICA DE JOGO COM API ---
    async function startGame(difficulty) {
        difficultyScreen.style.display = 'none';
        await fetch('/api/start', { method: 'POST' });
        document.addEventListener('keydown', handlePlayerInput);
        const speed = difficulty === 'Normal' ? 200 : 100;
        gameLoopInterval = setInterval(gameLoop, speed);
    }

    async function gameLoop() {
        const response = await fetch('/api/state');
        const gameState = await response.json();

        if (gameState.game_over) {
            clearInterval(gameLoopInterval);
            showGameOverScreen(gameState.score);
            return;
        }
        draw(gameState);
    }

    function draw(state) {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        ctx.fillStyle = 'lime';
        state.snake_body.forEach(segment => {
            ctx.fillRect(segment[0] * gridSize, segment[1] * gridSize, gridSize - 2, gridSize - 2);
        });
        ctx.fillStyle = 'red';
        const foodX = state.food_position[0];
        const foodY = state.food_position[1];
        ctx.fillRect(foodX * gridSize, foodY * gridSize, gridSize, gridSize);
        scoreElement.textContent = state.score;
    }

    async function handlePlayerInput(event) {
        const key = event.key;
        let direction = null;

        if (key === 'ArrowUp') direction = 'CIMA';
        if (key === 'ArrowDown') direction = 'BAIXO';
        if (key === 'ArrowLeft') direction = 'ESQUERDA';
        if (key === 'ArrowRight') direction = 'DIREITA';

        if (direction) {
            await fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction: direction })
            });
        }
    }

    function showGameOverScreen(finalScore) {
        finalScoreElement.textContent = finalScore;
        gameOverScreen.style.display = 'flex';
    }
});