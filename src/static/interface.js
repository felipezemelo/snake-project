// src/static/interface.js
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

    // --- Carregamento das Imagens dos Ratos ---
    // (Prepare as imagens 'rato_dourado.png' e 'rato_vermelho.png' na pasta 'static')
    const ratImages = {
        'NORMAL': new Image(),
        'DOURADO': new Image(),
        'VERMELHO': new Image()
    };
    ratImages['NORMAL'].src = "/static/rat.png";
    ratImages['DOURADO'].src = "/static/rato_dourado.png"; // Crie esta imagem
    ratImages['VERMELHO'].src = "/static/rato_vermelho.png"; // Crie esta imagem

    // Espera a imagem principal carregar antes de iniciar
    ratImages['NORMAL'].onload = () => {
        startScreen.classList.add('visible');
        document.addEventListener('keydown', handleKeyPress);
    };
    ratImages['NORMAL'].onerror = () => {
        console.error("Erro ao carregar a imagem 'rat.png'. Verifique se o ficheiro está na pasta 'src/static'.");
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
            if (index === 0) { /* ... (lógica dos olhos e língua continua igual) ... */ }
        });

        // --- LÓGICA DE DESENHAR O RATO CORRIGIDA ---
        const foodType = state.food.type;
        let foodImage = ratImages[foodType];

        // VERIFICAÇÃO: Se a imagem do power-up não carregou, usa a imagem do rato normal como fallback.
        if (!foodImage || !foodImage.complete || foodImage.naturalHeight === 0) {
            foodImage = ratImages['NORMAL'];
        }
        
        const foodX = state.food.position[0];
        const foodY = state.food.position[1];
        
        const ratSize = gridSize * 1.7 * pulseFactor;
        const offset = (gridSize - ratSize) / 2;

        if (foodImage && foodImage.complete) { // Desenha apenas se a imagem estiver carregada
            ctx.drawImage(foodImage, foodX * gridSize + offset, foodY * gridSize + offset, ratSize, ratSize);
        }
        
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