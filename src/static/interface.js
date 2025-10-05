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
    let tongueFrame = 0; // Para a animação da língua
    const particles = []; // Array para partículas da animação do fogo

    // --- Carregamento de TODAS as Imagens dos Ratos ---
    const ratImages = {
        'NORMAL': new Image(),
        'DOURADO': new Image(),
        'VERMELHO': new Image()
    };
    ratImages['NORMAL'].src = "/static/rat.png";
    ratImages['DOURADO'].src = "/static/rato_dourado.png";
    ratImages['VERMELHO'].src = "/static/rato_vermelho.png"; 

    // Espera TODAS as imagens carregarem antes de iniciar
    Promise.all([
        new Promise(resolve => { ratImages['NORMAL'].onload = resolve; ratImages['NORMAL'].onerror = resolve; }),
        new Promise(resolve => { ratImages['DOURADO'].onload = resolve; ratImages['DOURADO'].onerror = resolve; }),
        new Promise(resolve => { ratImages['VERMELHO'].onload = resolve; ratImages['VERMELHO'].onerror = resolve; })
    ]).then(() => {
        startScreen.classList.add('visible');
        document.addEventListener('keydown', handleKeyPress);
    });

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

    // Armazenar o estado anterior da cobra para detetar encolhimento
    let previousSnakeLength = 0; 

    async function startGame(difficulty) {
        difficultyScreen.classList.remove('visible');
        await fetch('/api/start', { method: 'POST' });
        document.addEventListener('keydown', handlePlayerInput);
        const speed = difficulty === 'Normal' ? 200 : 100;
        gameLoopInterval = setInterval(gameLoop, speed);
        previousSnakeLength = 3; // Inicia com o tamanho padrão da cobra
    }

    async function gameLoop() {
        // Animação da língua
        tongueFrame = (tongueFrame + 1) % 2; // Alterna entre 0 e 1

        // Animação de pulsação dos ratos
        pulseFactor = 1.0 + Math.sin(Date.now() / 200) * 0.15;
        
        const response = await fetch('/api/state');
        const gameState = await response.json();

        // Deteta se a cobra encolheu para gerar partículas
        if (gameState.snake_body.length < previousSnakeLength) {
            generateShrinkParticles(gameState.snake_body[0][0] * gridSize, gameState.snake_body[0][1] * gridSize);
        }
        previousSnakeLength = gameState.snake_body.length;

        if (gameState.game_over) {
            clearInterval(gameLoopInterval);
            document.removeEventListener('keydown', handlePlayerInput);
            showGameOverScreen(gameState.score);
            return;
        }
        draw(gameState);
        updateParticles(); // Atualiza a posição das partículas
        drawParticles();   // Desenha as partículas
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

            if (index === 0) { // Cabeça da cobra
                ctx.fillStyle = 'black';
                const eyeSize = 3;
                const direction = state.snake_direction;
                let eye1X, eye1Y, eye2X, eye2Y;
                let tongueX, tongueY, tongueW, tongueH;
                
                // Posição dos olhos
                if (direction === 'DIREITA') { eye1X = segX + gridSize - 8; eye1Y = segY + 4; eye2X = segX + gridSize - 8; eye2Y = segY + gridSize - 7; } 
                else if (direction === 'ESQUERDA') { eye1X = segX + 5; eye1Y = segY + 4; eye2X = segX + 5; eye2Y = segY + gridSize - 7; } 
                else if (direction === 'BAIXO') { eye1X = segX + 4; eye1Y = segY + gridSize - 8; eye2X = segX + gridSize - 7; eye2Y = segY + gridSize - 8; } 
                else { eye1X = segX + 4; eye1Y = segY + 5; eye2X = segX + gridSize - 7; eye2Y = segY + 5; }
                ctx.fillRect(eye1X, eye1Y, eyeSize, eyeSize);
                ctx.fillRect(eye2X, eye2Y, eyeSize, eyeSize);

                // Animação da língua
                if (tongueFrame === 1) { // Desenha a língua apenas em um frame para animação
                    ctx.fillStyle = 'red';
                    if (direction === 'DIREITA') { tongueX = segX + gridSize; tongueY = segY + gridSize / 2 - 1; tongueW = 5; tongueH = 2; }
                    else if (direction === 'ESQUERDA') { tongueX = segX - 5; tongueY = segY + gridSize / 2 - 1; tongueW = 5; tongueH = 2; }
                    else if (direction === 'BAIXO') { tongueX = segX + gridSize / 2 - 1; tongueY = segY + gridSize; tongueW = 2; tongueH = 5; }
                    else { tongueX = segX + gridSize / 2 - 1; tongueY = segY - 5; tongueW = 2; tongueH = 5; }
                    ctx.fillRect(tongueX, tongueY, tongueW, tongueH);
                }
            }
        });

        // --- LÓGICA DE DESENHAR O RATO ---
        const foodType = state.food.type;
        let foodImage = ratImages[foodType];

        // Se a imagem do power-up não carregou ou não existe, usa a imagem do rato normal como fallback.
        if (!foodImage || !foodImage.complete || foodImage.naturalHeight === 0) {
            foodImage = ratImages['NORMAL'];
        }
        
        const foodX = state.food.position[0];
        const foodY = state.food.position[1];
        
        // Aumenta o tamanho base dos ratos para 2.0 (antes era 1.7)
        const ratSize = gridSize * 2.0 * pulseFactor; 
        const offset = (gridSize - ratSize) / 2;

        if (foodImage && foodImage.complete) {
            ctx.drawImage(foodImage, foodX * gridSize + offset, foodY * gridSize + offset, ratSize, ratSize);
        }
        
        scoreElement.textContent = state.score;
    }

    // --- Funções de Partículas para o Rato Vermelho (Shrink Effect) ---
    function generateShrinkParticles(x, y) {
        for (let i = 0; i < 20; i++) { // 20 partículas
            particles.push({
                x: x + gridSize / 2,
                y: y + gridSize / 2,
                vx: (Math.random() - 0.5) * 4, // Velocidade X aleatória
                vy: (Math.random() - 0.5) * 4, // Velocidade Y aleatória
                color: `rgb(${Math.floor(Math.random() * 50) + 200}, ${Math.floor(Math.random() * 50)}, ${Math.floor(Math.random() * 50)})`, // Tons de vermelho/laranja
                life: 60, // Tempo de vida em frames
                size: Math.random() * 3 + 1 // Tamanho aleatório
            });
        }
    }

    function updateParticles() {
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life--;
            p.size *= 0.98; // Encolhe as partículas
            p.vy += 0.1; // Gravidade simples
            if (p.life <= 0 || p.size <= 0.5) {
                particles.splice(i, 1); // Remove partículas mortas
            }
        }
    }

    function drawParticles() {
        particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size / 2, 0, Math.PI * 2);
            ctx.fill();
        });
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