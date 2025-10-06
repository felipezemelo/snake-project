// src/static/interface.js
document.addEventListener('DOMContentLoaded', () => {
    const startScreen = document.getElementById('start-screen');
    const difficultyScreen = document.getElementById('difficulty-screen');
    const tutorialScreen = document.getElementById('tutorial-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const gameCanvas = document.getElementById('gameCanvas');
    const scoreElement = document.getElementById('score');
    
    // Elementos da tela de Game Over
    const finalScoresDiv = document.getElementById('final-scores');
    const newHighscoreDiv = document.getElementById('new-highscore-entry');
    const finalScoreElement = document.getElementById('finalScore');
    const highScoreListElement = document.getElementById('highScoreList');
    const playerNameInput = document.getElementById('playerNameInput');
    const saveScoreBtn = document.getElementById('saveScoreBtn');

    const restartBtn = document.getElementById('restartBtn');
    const normalBtn = document.getElementById('normalBtn');
    const dificilBtn = document.getElementById('dificilBtn');
    const playBtn = document.getElementById('playBtn');
    
    const ctx = gameCanvas.getContext('2d');
    const gridSize = 20;
    let gameLoopInterval;
    let pulseFactor = 1.0;
    let tongueFrame = 0;
    const particles = [];
    let previousSnakeLength = 0; 
    let proximaDirecao = null;

    window.currentSpeed = 200; // Valor inicial
    let currentDifficulty = 'Normal';

    const ratImages = {
        'NORMAL': new Image(),
        'DOURADO': new Image(),
        'VERMELHO': new Image()
    };
    ratImages['NORMAL'].src = "/static/rat.png";
    ratImages['DOURADO'].src = "/static/rato_dourado.png";
    ratImages['VERMELHO'].src = "/static/rato_vermelho.png"; 

    Promise.all([
        new Promise(resolve => { ratImages['NORMAL'].onload = resolve; ratImages['NORMAL'].onerror = resolve; }),
        new Promise(resolve => { ratImages['DOURADO'].onload = resolve; ratImages['DOURADO'].onerror = resolve; }),
        new Promise(resolve => { ratImages['VERMELHO'].onload = resolve; ratImages['VERMELHO'].onerror = resolve; })
    ]).then(() => {
        startScreen.classList.add('visible');
        document.addEventListener('keydown', handleKeyPress);
    });

    // --- LÓGICA DE NAVEGAÇÃO ---
    normalBtn.addEventListener('click', () => handleDifficultySelection('Normal'));
    dificilBtn.addEventListener('click', () => handleDifficultySelection('Difícil'));
    playBtn.addEventListener('click', () => startGame(playBtn.dataset.difficulty));
    restartBtn.addEventListener('click', () => location.reload());
    
    saveScoreBtn.addEventListener('click', () => {
        const finalScore = parseInt(finalScoreElement.textContent, 10);
        saveHighScore(finalScore);
    });

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

    function handleDifficultySelection(difficulty) {
        difficultyScreen.classList.remove('visible');
        tutorialScreen.classList.add('visible');
        playBtn.dataset.difficulty = difficulty;
    }

    async function startGame(difficulty) {
        tutorialScreen.classList.remove('visible');
        await fetch('/api/start', { method: 'POST' });
        
        currentDifficulty = difficulty;
        window.currentSpeed = difficulty === 'Normal' ? 200 : 100;

        proximaDirecao = null;
        document.addEventListener('keydown', handlePlayerInput);
        
        gameLoopInterval = setInterval(gameLoop, window.currentSpeed);
        previousSnakeLength = 3;
    }

    async function gameLoop() {
        if (proximaDirecao) {
            await fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction: proximaDirecao })
            });
            proximaDirecao = null;
        }

        tongueFrame = (tongueFrame + 1) % 2;
        pulseFactor = 1.0 + Math.sin(Date.now() / 200) * 0.15;
        
        const response = await fetch('/api/state');
        const gameState = await response.json();

        // --- LÓGICA DE AUMENTO DE VELOCIDADE CORRIGIDA ---
        if (currentDifficulty === 'Normal') {
            let newSpeed = window.currentSpeed;
            if (gameState.score >= 100 && window.currentSpeed > 120) {
                newSpeed = 120; // Nível 3
            } else if (gameState.score >= 50 && window.currentSpeed > 160) {
                newSpeed = 160; // Nível 2
            }

            if (newSpeed < window.currentSpeed) {
                window.currentSpeed = newSpeed;
                clearInterval(gameLoopInterval);
                gameLoopInterval = setInterval(gameLoop, window.currentSpeed);
            }
        }

        if (gameState.snake_body.length < previousSnakeLength) {
            generateShrinkParticles(gameState.snake_body[0][0] * gridSize, gameState.snake_body[0][1] * gridSize);
        }
        previousSnakeLength = gameState.snake_body.length;

        if (gameState.game_over) {
            showGameOverScreen(gameState.score);
            return;
        }
        draw(gameState);
        updateParticles();
        drawParticles();
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
                let eye1X, eye1Y, eye2X, eye2Y, tongueX, tongueY, tongueW, tongueH;
                
                if (direction === 'DIREITA') { eye1X = segX + gridSize - 8; eye1Y = segY + 4; eye2X = segX + gridSize - 8; eye2Y = segY + gridSize - 7; } 
                else if (direction === 'ESQUERDA') { eye1X = segX + 5; eye1Y = segY + 4; eye2X = segX + 5; eye2Y = segY + gridSize - 7; } 
                else if (direction === 'BAIXO') { eye1X = segX + 4; eye1Y = segY + gridSize - 8; eye2X = segX + gridSize - 7; eye2Y = segY + gridSize - 8; } 
                else { eye1X = segX + 4; eye1Y = segY + 5; eye2X = segX + gridSize - 7; eye2Y = segY + 5; }
                ctx.fillRect(eye1X, eye1Y, eyeSize, eyeSize);
                ctx.fillRect(eye2X, eye2Y, eyeSize, eyeSize);

                if (tongueFrame === 1) {
                    ctx.fillStyle = 'red';
                    if (direction === 'DIREITA') { tongueX = segX + gridSize; tongueY = segY + gridSize / 2 - 1; tongueW = 5; tongueH = 2; }
                    else if (direction === 'ESQUERDA') { tongueX = segX - 5; tongueY = segY + gridSize / 2 - 1; tongueW = 5; tongueH = 2; }
                    else if (direction === 'BAIXO') { tongueX = segX + gridSize / 2 - 1; tongueY = segY + gridSize; tongueW = 2; tongueH = 5; }
                    else { tongueX = segX + gridSize / 2 - 1; tongueY = segY - 5; tongueW = 2; tongueH = 5; }
                    ctx.fillRect(tongueX, tongueY, tongueW, tongueH);
                }
            }
        });

        const foodType = state.food.type;
        let foodImage = ratImages[foodType];
        if (!foodImage || !foodImage.complete || foodImage.naturalHeight === 0) foodImage = ratImages['NORMAL'];
        const foodX = state.food.position[0], foodY = state.food.position[1];
        const ratSize = gridSize * 2.0 * pulseFactor, offset = (gridSize - ratSize) / 2;
        if (foodImage && foodImage.complete) ctx.drawImage(foodImage, foodX * gridSize + offset, foodY * gridSize + offset, ratSize, ratSize);
        
        scoreElement.textContent = state.score;
    }

    function handlePlayerInput(event) {
        const key = event.key;
        let direction = null;
        if (key === 'ArrowUp') direction = 'CIMA';
        if (key === 'ArrowDown') direction = 'BAIXO';
        if (key === 'ArrowLeft') direction = 'ESQUERDA';
        if (key === 'ArrowRight') direction = 'DIREITA';
        if (direction) proximaDirecao = direction;
    }

    function showGameOverScreen(finalScore) {
        clearInterval(gameLoopInterval);
        document.removeEventListener('keydown', handlePlayerInput);
        finalScoreElement.textContent = finalScore;

        const highScores = JSON.parse(localStorage.getItem('snakeHighScores')) || [];
        const isNewHighScore = highScores.length < 5 || finalScore > highScores[highScores.length - 1].score;

        if (isNewHighScore) {
            finalScoresDiv.style.display = 'none';
            newHighscoreDiv.style.display = 'flex';
        } else {
            displayHighScores(highScores);
            finalScoresDiv.style.display = 'flex';
            newHighscoreDiv.style.display = 'none';
        }
        gameOverScreen.classList.add('visible');
    }

    function saveHighScore(finalScore) {
        const name = playerNameInput.value.trim().toUpperCase().substring(0, 3) || 'JOG';
        const highScores = JSON.parse(localStorage.getItem('snakeHighScores')) || [];
        
        highScores.push({ score: finalScore, name: name });
        highScores.sort((a, b) => b.score - a.score);
        highScores.splice(5);
        
        localStorage.setItem('snakeHighScores', JSON.stringify(highScores));
        
        newHighscoreDiv.style.display = 'none';
        finalScoresDiv.style.display = 'flex';
        displayHighScores(highScores);
    }

    function displayHighScores(scores) {
        highScoreListElement.innerHTML = '';
        if (scores.length > 0) {
            scores.forEach((score, index) => {
                const li = document.createElement('li');
                const nameSpan = document.createElement('span');
                nameSpan.className = 'score-name';
                nameSpan.textContent = `${index + 1}. ${score.name}`;
                const scoreSpan = document.createElement('span');
                scoreSpan.className = 'score-value';
                scoreSpan.textContent = score.score;
                li.appendChild(nameSpan);
                li.appendChild(scoreSpan);
                highScoreListElement.appendChild(li);
            });
        } else {
            highScoreListElement.innerHTML = '<li>Nenhum recorde ainda!</li>';
        }
    }
    
    function generateShrinkParticles(x, y) { for (let i = 0; i < 50; i++) particles.push({ x: x + gridSize / 2, y: y + gridSize / 2, vx: (Math.random() - 0.5) * 5, vy: (Math.random() - 0.5) * 5, color: `rgb(${Math.floor(Math.random()*50)+200}, ${Math.floor(Math.random()*50)}, ${Math.floor(Math.random()*50)})`, life: 80, size: Math.random() * 4 + 2 }); }
    function updateParticles() { for (let i = particles.length - 1; i >= 0; i--) { const p = particles[i]; p.x += p.vx; p.y += p.vy; p.life--; p.size *= 0.98; p.vy += 0.1; if (p.life <= 0 || p.size <= 0.5) particles.splice(i, 1); } }
    function drawParticles() { particles.forEach(p => { ctx.fillStyle = p.color; ctx.beginPath(); ctx.arc(p.x, p.y, p.size / 2, 0, Math.PI * 2); ctx.fill(); }); }
    function drawRoundedRect(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();ctx.fill();}
});