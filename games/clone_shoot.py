import streamlit as st
import streamlit.components.v1 as components

def clone_shoot_game():
    st.header("👥 クローン・シュート")
    st.write("ゲートで軍勢を増やせ！兵士たちは自動で敵を撃つぞ！")
    game_html = """
    <div id="game-container" style="text-align: center; background: #222; padding: 15px; border-radius: 15px; position: relative;">
        <canvas id="gateCanvas" width="400" height="500" style="background: #eee; border: 3px solid #333; cursor: pointer;"></canvas>
        <div style="color: white; font-family: sans-serif; margin-top: 10px; font-size: 24px; font-weight: bold;">
            SOLDIERS: <span id="count">10</span>
        </div>
    </div>
    <script>
    const canvas = document.getElementById('gateCanvas'); const ctx = canvas.getContext('2d');
    const countElement = document.getElementById('count');
    let soldiers = 10, playerX = 180, distance = 0, gameActive = false, frameCount = 0;
    let gameStarted = false;
    const goalDistance = 4500, gates = [], enemySwarms = [], bullets = [];
    function createObjects() {
        gates.length = 0; enemySwarms.length = 0; bullets.length = 0;
        for(let i = 1; i < 15; i++) {
            let y = -i * 300;
            let g1 = { type: Math.random() > 0.4 ? 'add' : 'mul', val: 0 };
            g1.val = g1.type === 'add' ? Math.floor(Math.random() * 15) + 5 : 2;
            let g2 = { type: Math.random() > 0.7 ? 'sub' : 'add', val: 0 };
            g2.val = g2.type === 'sub' ? Math.floor(Math.random() * 8) + 1 : Math.floor(Math.random() * 5) + 1;
            let side = Math.random() > 0.5;
            let leftG = side ? g1 : g2; let rightG = side ? g2 : g1;
            gates.push({ x: 0, y: y, w: 200, h: 40, type: leftG.type, val: leftG.val, text: leftG.type==='mul'?'x'+leftG.val:(leftG.type==='sub'?'-':'+')+leftG.val, color: leftG.type==='sub'?'#ef4444':'#3b82f6' });
            gates.push({ x: 200, y: y, w: 200, h: 40, type: rightG.type, val: rightG.val, text: rightG.type==='mul'?'x'+rightG.val:(rightG.type==='sub'?'-':'+')+rightG.val, color: rightG.type==='sub'?'#ef4444':'#3b82f6' });
            if(i % 2 === 0) {
                let baseHp = Math.floor(5 + (i * i * 3.5)); let randomHp = Math.floor(Math.random() * (i * 10)) + baseHp;
                let size = 30 + Math.min(randomHp / 10, 50);
                enemySwarms.push({ x: Math.random() * 300, y: y + 150, hp: randomHp, size: size });
            }
        }
    }
    createObjects();
    function startGame() { if(!gameStarted) { gameStarted = true; gameActive = true; } }
    window.addEventListener("keydown", (e) => { startGame(); if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true; if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true; });
    window.addEventListener("keyup", (e) => { if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false; if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false; });
    canvas.addEventListener('click', startGame);
    let leftPressed = false, rightPressed = false;
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ddd"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        if(!gameStarted) {
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white"; ctx.font = "bold 25px Arial"; ctx.textAlign = "center";
            ctx.fillText("最強の軍勢を作れ！", canvas.width/2, canvas.height/2 - 20);
            ctx.font = "18px Arial"; ctx.fillText("CLICK or PRESS ANY KEY", canvas.width/2, canvas.height/2 + 30);
            requestAnimationFrame(draw); return;
        }
        if(!gameActive) return; frameCount++; distance += 4.0; ctx.textAlign = "left"; 
        ctx.fillStyle = "#3b82f6"; for(let i = 0; i < Math.min(soldiers, 60); i++) { let offsetX = (i % 6) * 7 - 15; let offsetY = Math.floor(i / 6) * 7; ctx.beginPath(); ctx.arc(playerX + 20 + offsetX, 450 - offsetY, 3, 0, Math.PI*2); ctx.fill(); }
        if(leftPressed && playerX > 0) playerX -= 6; if(rightPressed && playerX < canvas.width - 40) playerX += 6;
        if(frameCount % 18 === 0 && soldiers > 0) { for(let i = 0; i < soldiers; i++) { let offsetX = (i % 10) * 6 - 27; let offsetY = Math.floor(i / 10) * 5; bullets.push({ x: playerX + 20 + offsetX, y: 430 - offsetY, r: 2, speed: 12 }); } }
        ctx.fillStyle = "#222"; for(let i = bullets.length - 1; i >= 0; i--) { let b = bullets[i]; b.y -= b.speed; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2); ctx.fill(); if(b.y < 0) bullets.splice(i, 1); }
        gates.forEach((g, index) => {
            let currentY = g.y + distance;
            if(currentY > -100 && currentY < 600) {
                ctx.fillStyle = g.color; ctx.globalAlpha = 0.6; ctx.fillRect(g.x, currentY, g.w, g.h); ctx.globalAlpha = 1.0; ctx.fillStyle = "white"; ctx.font = "bold 20px Arial"; ctx.fillText(g.text, g.x + 80, currentY + 28);
                if(currentY > 410 && currentY < 450 && playerX + 20 > g.x && playerX + 20 < g.x + g.w) {
                    if(g.type === 'add') soldiers += g.val; else if(g.type === 'mul') soldiers *= g.val; else if(g.type === 'sub') soldiers = Math.max(1, soldiers - g.val);
                    countElement.innerText = soldiers; gates.splice(index, 1);
                }
            }
        });
        enemySwarms.forEach((s, index) => {
            let currentY = s.y + distance;
            if(currentY > -100 && currentY < 600) {
                if (currentY < 430) { if (s.x < playerX) s.x += 1.2; else if (s.x > playerX) s.x -= 1.2; }
                ctx.fillStyle = "#ef4444"; ctx.beginPath(); ctx.arc(s.x + s.size/2, currentY + s.size/2, s.size/2, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = "white"; ctx.font = "bold 16px Arial"; ctx.fillText(s.hp, s.x + s.size/2 - 8, currentY + s.size/2 + 6);
                bullets.forEach((b, bIndex) => { if(b.x > s.x && b.x < s.x + s.size && b.y > currentY && b.y < currentY + s.size) { s.hp--; bullets.splice(bIndex, 1); if(s.hp <= 0) enemySwarms.splice(index, 1); } });
                if(currentY > 400 && currentY < 460 && playerX + 40 > s.x && playerX < s.x + s.size) {
                    soldiers = Math.max(0, soldiers - s.hp); countElement.innerText = soldiers; enemySwarms.splice(index, 1);
                    if (soldiers <= 0) { gameActive = false; alert("軍勢が全滅しました..."); location.reload(); }
                }
            }
        });
        if(distance > 4500) { gameActive = false; if(soldiers >= 1000) alert("VICTORY!"); else alert("DEFEAT..."); location.reload(); }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=600)
