import streamlit as st
import streamlit.components.v1 as components

def invader_game():
    st.header("👾 インベーダー・クエスト PRO")
    game_html = """
    <div id="game-container" style="text-align: center; background: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #333;">
        <canvas id="gameCanvas" width="400" height="400" style="background: black; border: 1px solid #444;"></canvas>
        <div style="display: flex; justify-content: space-around; color: #00FF00; font-family: 'Courier New', monospace; margin-top: 15px; background: #000; padding: 10px; border-radius: 5px;">
            <div>SCORE: <span id="score">0</span></div><div>SHOTS: <span id="shots">0</span></div><div>TIME: <span id="timer">0.0</span>s</div>
        </div>
    </div>
    <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const scoreElement = document.getElementById('score');
    const shotsElement = document.getElementById('shots');
    const timerElement = document.getElementById('timer');
    
    let score = 0, shotsFired = 0, enemiesDefeated = 0;
    let startTime = Date.now();
    let gameActive = false, gameStarted = false, isVisible = true;
    
    const player = { x: 180, y: 370, w: 40, h: 20, speed: 5 };
    const bullets = [];
    const enemies = [];
    
    function initEnemies() {
        enemies.length = 0;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 6; j++) {
                enemies.push({ x: j * 50 + 50, y: i * 40 + 30, w: 30, h: 20, alive: true });
            }
        }
    }
    initEnemies();
    
    function startGame() {
        if(!gameStarted) {
            gameStarted = true;
            gameActive = true;
            startTime = Date.now();
            initEnemies();
        }
    }
    
    let rightPressed = false, leftPressed = false, spacePressed = false;
    
    window.addEventListener("keydown", (e) => {
        startGame();
        if(!gameActive) return;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
        if(e.key == " " || e.code == "Space") {
            if (!spacePressed) {
                bullets.push({ x: player.x + 18, y: player.y, r: 3, speed: 8 });
                shotsFired++;
                score = Math.max(0, score - 5);
                shotsElement.innerText = shotsFired;
            }
            spacePressed = true;
            e.preventDefault();
        }
    });
    
    window.addEventListener("keyup", (e) => {
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        if(e.key == " ") spacePressed = false;
    });
    
    canvas.addEventListener('click', startGame);
    document.addEventListener('visibilitychange', () => { isVisible = !document.hidden; });
    
    let enemyDirection = 1, enemyMoveCounter = 0;
    
    function calculateFinalScore() {
        let timeElapsed = (Date.now() - startTime) / 1000;
        let accuracy = shotsFired > 0 ? (enemiesDefeated / shotsFired) : 0;
        let timeBonus = Math.max(0, 1000 - Math.floor(timeElapsed * 10));
        let accuracyBonus = Math.floor(accuracy * 1000);
        return score + accuracyBonus + timeBonus;
    }
    
    function draw() {
        if(!isVisible) {
            requestAnimationFrame(draw);
            return;
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        if(!gameStarted) {
            ctx.fillStyle = "rgba(0,0,0,0.8)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00FF00";
            ctx.font = "bold 20px Arial";
            ctx.textAlign = "center";
            ctx.fillText("INVADER QUEST", canvas.width/2, canvas.height/2 - 20);
            ctx.font = "14px Arial";
            ctx.fillText("CLICK or PRESS ANY KEY", canvas.width/2, canvas.height/2 + 20);
            requestAnimationFrame(draw);
            return;
        }
        
        if(!gameActive) {
            requestAnimationFrame(draw);
            return;
        }
        
        let timeElapsed = (Date.now() - startTime) / 1000;
        timerElement.innerText = timeElapsed.toFixed(1);
        
        // プレイヤー描画
        ctx.fillStyle = "#00FF00";
        ctx.fillRect(player.x, player.y, player.w, player.h);
        
        // プレイヤー移動
        if(rightPressed && player.x < canvas.width - player.w) player.x += player.speed;
        if(leftPressed && player.x > 0) player.x -= player.speed;
        
        // 弾丸描画と移動
        ctx.fillStyle = "yellow";
        for(let i = bullets.length - 1; i >= 0; i--) {
            let b = bullets[i];
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fill();
            b.y -= b.speed;
            if(b.y < 0) bullets.splice(i, 1);
        }
        
        // 敵の処理
        let edgeReached = false, aliveCount = 0;
        enemies.forEach(e => {
            if (!e.alive) return;
            aliveCount++;
            ctx.fillStyle = "red";
            ctx.fillRect(e.x, e.y, e.w, e.h);
            
            // 弾丸との衝突判定
            bullets.forEach((b, bIndex) => {
                if (b.x > e.x && b.x < e.x + e.w && b.y > e.y && b.y < e.y + e.h) {
                    e.alive = false;
                    bullets.splice(bIndex, 1);
                    enemiesDefeated++;
                    score += 100;
                    scoreElement.innerText = score;
                }
            });
            
            // 端に到達したかチェック
            if (enemyMoveCounter > 25) {
                if (e.x + 10 * enemyDirection > canvas.width - e.w || e.x + 10 * enemyDirection < 0) {
                    edgeReached = true;
                }
            }
        });
        
        // 敵の移動
        if (enemyMoveCounter > 25) {
            if (edgeReached) {
                enemyDirection *= -1;
                enemies.forEach(e => e.y += 20);
            } else {
                enemies.forEach(e => e.x += 10 * enemyDirection);
            }
            enemyMoveCounter = 0;
        }
        enemyMoveCounter++;
        
        // ゲーム終了条件
        if (enemies.some(e => e.alive && e.y > 350)) {
            gameActive = false;
            alert("GAME OVER!");
            location.reload();
        }
        if (aliveCount === 0) {
            gameActive = false;
            alert("MISSION COMPLETE! Score: " + calculateFinalScore());
            location.reload();
        }
        
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=550)
