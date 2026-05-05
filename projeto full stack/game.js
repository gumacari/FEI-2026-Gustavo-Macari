// Pega o elemento canvas e o contexto 2D para desenhar o jogo:
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');

// Estado principal do jogo com todas as variáveis usadas:
const state = {
    score: 0,
    gameOver: false,
    keys: { left: false, right: false, shoot: false },
    player: { x: canvas.width / 2 - 40, y: canvas.height - 90, width: 80, height: 100, speed: 6, shootCooldown: 0 },
    bullets: [],
    enemies: [],
    spawnTimer: 0,
};

// Carrega imagens da nave e do alien, salvas em assets:
const alienImage = new Image();
const shipImage = new Image();
alienImage.src = 'assets/alien.png';
shipImage.src = 'assets/ship.png';

// Desenha tudo na tela: fundo, jogador, tiros, inimigos e pontuação:
function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Desenha a nave do jogador. Se a imagem não existir, desenha um triângulo verde:
    if (shipImage.complete && shipImage.naturalHeight !== 0) {
        ctx.drawImage(shipImage, state.player.x, state.player.y, state.player.width, state.player.height);
    } else {
        ctx.fillStyle = '#4cff00';
        ctx.beginPath();
        ctx.moveTo(state.player.x + state.player.width / 2, state.player.y);
        ctx.lineTo(state.player.x + state.player.width, state.player.y + state.player.height);
        ctx.lineTo(state.player.x, state.player.y + state.player.height);
        ctx.closePath();
        ctx.fill();
    }

    // Desenha os tiros em amarelo:
    ctx.fillStyle = '#ffeb3b';
    state.bullets.forEach((bullet) => ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height));

    // Desenha os inimigos. Se não houver imagem, desenha um quadrado vermelho:
    state.enemies.forEach((enemy) => {
        if (alienImage.complete && alienImage.naturalHeight !== 0) {
            ctx.drawImage(alienImage, enemy.x, enemy.y, enemy.width, enemy.height);
        } else {
            ctx.fillStyle = '#ff1744';
            ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        }
    });

    // Mostra a pontuação na tela HTML:
    scoreElement.textContent = state.score;

    // Se o jogo acabou, mostra mensagem de Game Over:
    if (state.gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 40px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over', canvas.width / 2, canvas.height / 2 - 20);
        ctx.font = '20px Arial';
        ctx.fillText(`Pontuação final: ${state.score}`, canvas.width / 2, canvas.height / 2 + 20);
    }
}

// Atualiza as posições e o estado do jogo a cada frame:
function update() {
    if (state.gameOver) return;

    // Movimento do jogador para esquerda e direita:
    if (state.keys.left && state.player.x > 0) {
        state.player.x -= state.player.speed;
    }
    if (state.keys.right && state.player.x + state.player.width < canvas.width) {
        state.player.x += state.player.speed;
    }

    // Tiro do jogador, com tempo de recarga:
    if (state.keys.shoot && state.player.shootCooldown <= 0) {
        state.bullets.push({ x: state.player.x + state.player.width / 2 - 3, y: state.player.y - 12, width: 6, height: 12, speed: 10 });
        state.player.shootCooldown = 18;
    }
    if (state.player.shootCooldown > 0) state.player.shootCooldown -= 1;

    // Move os tiros para cima e remove os que saem da tela:
    for (let i = state.bullets.length - 1; i >= 0; i -= 1) {
        state.bullets[i].y -= state.bullets[i].speed;
        if (state.bullets[i].y + state.bullets[i].height < 0) {
            state.bullets.splice(i, 1);
        }
    }

    // Cria novos inimigos aos poucos:
    if (state.spawnTimer <= 0) {
        const size = 56;
        state.enemies.push({ x: Math.random() * (canvas.width - size), y: -size, width: size, height: size, speed: 1 + Math.random() * 1.2 });
        state.spawnTimer = 70;
    } else {
        state.spawnTimer -= 1;
    }

    // Move inimigos para baixo, verifica fim de jogo e colisões com tiros:
    for (let i = state.enemies.length - 1; i >= 0; i -= 1) {
        const enemy = state.enemies[i];
        enemy.y += enemy.speed;

        if (enemy.y + enemy.height >= canvas.height) {
            state.gameOver = true;
        }

        for (let j = state.bullets.length - 1; j >= 0; j -= 1) {
            const bullet = state.bullets[j];
            if (bullet.x < enemy.x + enemy.width && bullet.x + bullet.width > enemy.x && bullet.y < enemy.y + enemy.height && bullet.y + bullet.height > enemy.y) {
                state.enemies.splice(i, 1);
                state.bullets.splice(j, 1);
                state.score += 10;
                break;
            }
        }
    }
}

// Função que roda o jogo repetidamente usando requestAnimationFrame:
function loop() {
    update();
    draw();
    if (!state.gameOver) requestAnimationFrame(loop);
}

// Configura as teclas usadas no jogo: esquerda, direita e espaço:
function setupControls() {
    document.addEventListener('keydown', (event) => {
        if (event.code === 'ArrowLeft') state.keys.left = true;
        if (event.code === 'ArrowRight') state.keys.right = true;
        if (event.code === 'Space') state.keys.shoot = true;
    });

    document.addEventListener('keyup', (event) => {
        if (event.code === 'ArrowLeft') state.keys.left = false;
        if (event.code === 'ArrowRight') state.keys.right = false;
        if (event.code === 'Space') state.keys.shoot = false;
    });
}

setupControls();
loop();