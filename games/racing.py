import streamlit as st
import streamlit.components.v1 as components

def racing_game():
    st.header("🏎️ マリオカート風レーシング")
    st.write("左右キーでハンドル操作！ライバル車を避けてコインを集め、パワーアップをゲットせよ！")
    game_html = """
    <div id="game-container" style="text-align: center; background: #333; padding: 15px; border-radius: 15px;">
        <canvas id="raceCanvas" width="500" height="600" style="background: #87CEEB; border: 3px solid #555; cursor: pointer;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('raceCanvas');
    const ctx = canvas.getContext('2d');
    
    let gameActive = false, gameStarted = false, frameCount = 0;
    let score = 0, speed = 6, distance = 0, playerLane = 1;
    
    const lanes = [100, 200, 300, 400];
    const player = { x: lanes[1], y: 500, w: 50, h: 80, lane: 1 };
    const enemies = [];
    const coins = [];
    const powerups = [];
    
    function createEnemy() {
        let lane = Math.floor(Math.random() * 4);
        enemies.push({
            x: lanes[lane], y: -150, w: 50, h: 80,
            lane: lane, speed: Math.random() * 2 + 3
        });
    }
    
    function createCoin() {
        let lane = Math.floor(Math.random() * 4);
        coins.push({ x: lanes[lane] + 25, y: -50, r: 15, lane: lane });
    }
    
    function createPowerup() {
        let lane = Math.floor(Math.random() * 4);
        powerups.push({
            x: lanes[lane] + 25, y: -50, r: 20, lane: lane,
            type: Math.random() > 0.5 ? 'speed' : 'shield'
        });
    }
    
    let keys = {}, lastKey = null;
    
    function startGame() {
        if(!gameStarted) {
            gameStarted = true;
            gameActive = true;
        }
    }
    
    window.addEventListener("keydown", e => {
        startGame();
        if(e.code === "ArrowRight" && lastKey !== "ArrowRight" && playerLane < 3) {
            playerLane++;
            lastKey = "ArrowRight";
        }
        if(e.code === "ArrowLeft" && lastKey !== "ArrowLeft" && playerLane > 0) {
            playerLane--;
            lastKey = "ArrowLeft";
        }
        if(["ArrowLeft", "ArrowRight", "Space"].includes(e.code)) e.preventDefault();
    });
    
    window.addEventListener("keyup", e => {
        if(e.code === "ArrowLeft" || e.code === "ArrowRight") lastKey = null;
    });
    
    canvas.addEventListener('click', startGame);
    
    let isVisible = true;
    document.addEventListener('visibilitychange', () => { isVisible = !document.hidden; });
    
    function drawRoad() {
        ctx.fillStyle = "#555";
        ctx.fillRect(50, 0, 400, canvas.height);
        ctx.strokeStyle = "yellow";
        ctx.setLineDash([30, 30]);
        ctx.lineDashOffset = -distance;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(canvas.width/2, 0);
        ctx.lineTo(canvas.width/2, canvas.height);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.strokeStyle = "white";
        ctx.lineWidth = 2;
        for(let i = 0; i < 4; i++) {
            ctx.beginPath();
            ctx.moveTo(50 + (i * 100), 0);
            ctx.lineTo(50 + (i * 100), canvas.height);
            ctx.stroke();
        }
    }
    
    function draw() {
        if(!isVisible) {
            requestAnimationFrame(draw);
            return;
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#654321";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        drawRoad();
        
        if(!gameStarted) {
            ctx.fillStyle = "rgba(0,0,0,0.6)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.font = "bold 30px Arial";
            ctx.textAlign = "center";
            ctx.fillText("🏎️ RACING GAME", canvas.width/2, canvas.height/2 - 20);
            ctx.font = "18px Arial";
            ctx.fillText("CLICK or PRESS ANY KEY", canvas.width/2, canvas.height/2 + 30);
            requestAnimationFrame(draw);
            return;
        }
        
        if(!gameActive) {
            requestAnimationFrame(draw);
            return;
        }
        
        frameCount++;
        distance += speed;
        
        // オブジェクト生成
        if(frameCount % 80 === 0) createEnemy();
        if(frameCount % 120 === 0) createCoin();
        if(frameCount % 200 === 0) createPowerup();
        
        speed = 6 + Math.floor(score / 500);
        player.x += (lanes[playerLane] - player.x) * 0.2;
        
        // 敵処理
        ctx.fillStyle = "red";
        for(let i = enemies.length - 1; i >= 0; i--) {
            let e = enemies[i];
            e.y += speed;
            ctx.fillRect(e.x, e.y, e.w, e.h);
            ctx.fillStyle = "darkred";
            ctx.fillRect(e.x + 5, e.y + 10, 40, 20);
            ctx.fillStyle = "red";
            
            // 衝突判定
            if(player.x < e.x + e.w && player.x + player.w > e.x &&
               player.y < e.y + e.h && player.y + player.h > e.y) {
                gameActive = false;
                alert("クラッシュ！ SCORE: " + score);
                location.reload();
            }
            if(e.y > canvas.height) enemies.splice(i, 1);
        }
        
        // コイン処理
        ctx.fillStyle = "gold";
        for(let i = coins.length - 1; i >= 0; i--) {
            let c = coins[i];
            c.y += speed;
            ctx.beginPath();
            ctx.arc(c.x, c.y, c.r, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = "yellow";
            ctx.beginPath();
            ctx.arc(c.x, c.y, c.r - 3, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = "gold";
            
            // 取得判定
            if(Math.hypot(player.x + 25 - c.x, player.y + 40 - c.y) < 35) {
                score += 50;
                coins.splice(i, 1);
            }
            if(c.y > canvas.height) coins.splice(i, 1);
        }
        
        // パワーアップ処理
        ctx.fillStyle = "purple";
        for(let i = powerups.length - 1; i >= 0; i--) {
            let p = powerups[i];
            p.y += speed;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = "white";
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(p.type === 'speed' ? '⚡' : '🛡️', p.x, p.y + 5);
            ctx.fillStyle = "purple";
            
            // 取得判定
            if(Math.hypot(player.x + 25 - p.x, player.y + 40 - p.y) < 40) {
                if(p.type === 'speed') {
                    speed += 2;
                    score += 200;
                } else {
                    score += 300;
                }
                powerups.splice(i, 1);
            }
            if(p.y > canvas.height) powerups.splice(i, 1);
        }
        
        // プレイヤー描画
        ctx.fillStyle = "blue";
        ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.fillStyle = "lightblue";
        ctx.fillRect(player.x + 8, player.y + 15, 34, 25);
        
        // UI表示
        ctx.fillStyle = "white";
        ctx.font = "bold 20px Arial";
        ctx.textAlign = "left";
        ctx.fillText("SCORE: " + score, 10, 30);
        ctx.fillText("SPEED: " + (speed * 15) + "km/h", 10, 60);
        ctx.fillText("DISTANCE: " + Math.floor(distance / 10) + "m", 10, 90);
        
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=650)
