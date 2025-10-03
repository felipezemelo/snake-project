// src/static/game.js
document.addEventListener('DOMContentLoaded', () => {
    const startScreen = document.getElementById('start-screen');
    const difficultyScreen = document.getElementById('difficulty-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const gameCanvas = document.getElementById('gameCanvas');
    const scoreElement = document.getElementById('score');
    const finalScoreElement = document.getElementById('finalScore');
    const restartBtn = document.getElementById('restartBtn');
    const normalBtn = document.getElementById('normalBtn');
    const dificilBtn = document.getElementById('dificilBtn');
    const ctx = gameCanvas.getContext('2d');
    const gridSize = 20;
    let gameLoopInterval;
    let pulseFactor = 1.0;

    const ratImage = new Image();
    ratImage.src = "/static/rat.png";

    ratImage.onload = () => {
        startScreen.classList.add('visible');
        document.addEventListener('keydown', handleKeyPress);
    };
    ratImage.onerror = () => {
        console.error("Erro ao carregar a imagem do rato. Verifique se o ficheiro 'rat.png' está na pasta 'src/static'.");
    };

    normalBtn.addEventListener('click', () => startGame('Normal'));
    dificilBtn.addEventListener('click', () => startGame('Dificil'));
    restartBtn.addEventListener('click', () => location.reload());

    function handleKeyPress(event) {
        if (startScreen.classList.contains('visible')) {
            showDifficultyScreen();
            document.removeEventListener('keydown', handleKeyPress);
        }
    }

    function showDifficultyScreen() {
        startScreen.classList.remove('visible');
        difficultyScreen.classList.add('visible');
    }

    async function startGame(difficulty) {
        difficultyScreen.classList.remove('visible');
        await fetch('/api/start', { method: 'POST' });
        document.addEventListener('keydown', handlePlayerInput);
        const speed = difficulty === 'Normal' ? 200 : 100;
        gameLoopInterval = setInterval(gameLoop, speed);
    }

    async function gameLoop() {
        pulseFactor = 1.0 + Math.sin(Date.now() / 200) * 0.15;
        const response = await fetch('/api/state');
        const gameState = await response.json();
        if (gameState.game_over) {
            clearInterval(gameLoopInterval);
            document.removeEventListener('keydown', handlePlayerInput);
            showGameOverScreen(gameState.score);
            return;
        }
        draw(gameState);
    }
    
    function drawRoundedRect(x, y, width, height, radius) {
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        ctx.lineTo(x + radius, y + height);
        ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        ctx.lineTo(x, y + radius);
        ctx.quadraticCurveTo(x, y, x + radius, y);
        ctx.closePath();
        ctx.fill();
    }

    function draw(state) {
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        state.snake_body.forEach((segment, index) => {
            const segX = segment[0] * gridSize;
            const segY = segment[1] * gridSize;

            ctx.fillStyle = (index === 0) ? '#39FF14' : 'lime';
            drawRoundedRect(segX + 1, segY + 1, gridSize - 2, gridSize - 2, 5);

            if (index === 0) {
                ctx.fillStyle = 'black';
                const eyeSize = 3;
                const direction = state.snake_direction;
                let eye1X, eye1Y, eye2X, eye2Y;

                if (direction === 'DIREITA') {
                    eye1X = segX + gridSize - 8; eye1Y = segY + 4;
                    eye2X = segX + gridSize - 8; eye2Y = segY + gridSize - 7;
                } else if (direction === 'ESQUERDA') {
                    eye1X = segX + 5; eye1Y = segY + 4;
                    eye2X = segX + 5; eye2Y = segY + gridSize - 7;
                } else if (direction === 'BAIXO') {
                    eye1X = segX + 4; eye1Y = segY + gridSize - 8;
                    eye2X = segX + gridSize - 7; eye2Y = segY + gridSize - 8;
                } else { // CIMA
                    eye1X = segX + 4; eye1Y = segY + 5;
                    eye2X = segX + gridSize - 7; eye2Y = segY + 5;
                }
                ctx.fillRect(eye1X, eye1Y, eyeSize, eyeSize);
                ctx.fillRect(eye2X, eye2Y, eyeSize, eyeSize);

                // --- LÓGICA DA LÍNGUA ---
                // 10% de chance de mostrar a língua neste frame
                if (Math.random() < 0.1) {
                    ctx.fillStyle = 'red';
                    let tongueX, tongueY, tongueWidth, tongueHeight;
                    const tongueLength = 8;

                    if (direction === 'DIREITA') {
                        tongueX = segX + gridSize;
                        tongueY = segY + (gridSize / 2) - 1;
                        tongueWidth = tongueLength;
                        tongueHeight = 2;
                    } else if (direction === 'ESQUERDA') {
                        tongueX = segX - tongueLength;
                        tongueY = segY + (gridSize / 2) - 1;
                        tongueWidth = tongueLength;
                        tongueHeight = 2;
                    } else if (direction === 'BAIXO') {
                        tongueX = segX + (gridSize / 2) - 1;
                        tongueY = segY + gridSize;
                        tongueWidth = 2;
                        tongueHeight = tongueLength;
                    } else { // CIMA
                        tongueX = segX + (gridSize / 2) - 1;
                        tongueY = segY - tongueLength;
                        tongueWidth = 2;
                        tongueHeight = tongueLength;
                    }
                    ctx.fillRect(tongueX, tongueY, tongueWidth, tongueHeight);
                }
            }
        });

        const foodX = state.food_position[0];
        const foodY = state.food_position[1];
        const ratSize = gridSize * 1.7 * pulseFactor;
        const offset = (gridSize - ratSize) / 2;
        ctx.drawImage(ratImage, foodX * gridSize + offset, foodY * gridSize + offset, ratSize, ratSize);
        
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
        gameOverScreen.classList.add('visible');
    }
});