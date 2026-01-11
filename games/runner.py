import streamlit as st
import streamlit.components.v1 as components

def side_scroller_game():
    st.header("🏃 ブロック・ランナー")
    st.write("左右キーで移動、スペースキーでジャンプ！敵を踏んでゴールを目指せ！")
    game_html = """
    <div id="game-container" style="text-align: center; background: #87CEEB; padding: 15px; border-radius: 15px;">
        <canvas id="sideCanvas" width="600" height="400" style="background: #87CEEB; border: 3px solid #333; cursor: pointer;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('sideCanvas'); const ctx = canvas.getContext('2d');
    let gameActive = false, gameStarted = false, cameraX = 0;
    const player = { x: 50, y: 300, w: 30, h: 30, vx: 0, vy: 0, speed: 5, jumpForce: -13, grounded: false };
    const gravity = 0.6, platforms = [
        {x: 0, y: 350, w: 400, h: 50}, {x: 500, y: 350, w: 300, h: 50}, {x: 900, y: 350, w: 1000, h: 50},
        {x: 200, y: 250, w: 100, h: 20}, {x: 400, y: 200, w: 100, h: 20}, {x: 700, y: 250, w: 150, h: 20},
        {x: 1100, y: 200, w: 200, h: 20}, {x: 1400, y: 250, w: 100, h: 20}
    ];
    const enemies = [
        {x: 600, y: 320, w: 30, h: 30, vx: -2, alive: true}, {x: 1200, y: 320, w: 30, h: 30, vx: -2, alive: true}, {x: 1500, y: 320, w: 30, h: 30, vx: -2, alive: true}
    ];
    const goal = {x: 1800, y: 250, w: 40, h: 100}, keys = {};
    function startGame() { if(!gameStarted) { gameStarted = true; gameActive = true; } }
    window.addEventListener("keydown", e => { startGame(); keys[e.code] = true; if(e.code === "Space") e.preventDefault(); });
    window.addEventListener("keyup", e => keys[e.code] = false);
    canvas.addEventListener('click', startGame);
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if(!gameStarted) {
            ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white"; ctx.font = "bold 25px Arial"; ctx.textAlign = "center";
            ctx.fillText("BLOCK RUNNER", canvas.width/2, canvas.height/2 - 20);
            ctx.font = "18px Arial"; ctx.fillText("CLICK or PRESS ANY KEY", canvas.width/2, canvas.height/2 + 30);
            requestAnimationFrame(draw); return;
        }
        if(!gameActive) return;
        if(keys["ArrowRight"]) player.vx = player.speed; else if(keys["ArrowLeft"]) player.vx = -player.speed; else player.vx = 0;
        if(keys["Space"] && player.grounded) { player.vy = player.jumpForce; player.grounded = false; }
        player.vy += gravity; player.x += player.vx; player.y += player.vy; player.grounded = false;
        platforms.forEach(p => {
            if(player.x < p.x + p.w && player.x + player.w > p.x && player.y < p.y + p.h && player.y + player.h > p.y) {
                if(player.vy > 0 && player.y + player.h - player.vy <= p.y) { player.y = p.y - player.h; player.vy = 0; player.grounded = true; }
            }
        });
        if(player.x > canvas.width / 2) cameraX = player.x - canvas.width / 2;
        ctx.save(); ctx.translate(-cameraX, 0);
        ctx.fillStyle = "#654321"; ctx.fillRect(0, 350, 2000, 100);
        ctx.fillStyle = "#4CAF50"; platforms.forEach(p => ctx.fillRect(p.x, p.y, p.w, p.h));
        enemies.forEach(e => {
            if(!e.alive) return; e.x += e.vx; if(e.x < 500 || e.x > 1850) e.vx *= -1;
            ctx.fillStyle = "red"; ctx.fillRect(e.x, e.y, e.w, e.h);
            if(player.x < e.x + e.w && player.x + player.w > e.x && player.y < e.y + e.h && player.y + player.h > e.y) {
                if(player.vy > 0 && player.y + player.h - player.vy <= e.y) { e.alive = false; player.vy = -10; }
                else { gameActive = false; alert("GAME OVER!"); location.reload(); }
            }
        });
        ctx.fillStyle = "gold"; ctx.fillRect(goal.x, goal.y, goal.w, goal.h);
        if(player.x < goal.x + goal.w && player.x + player.w > goal.x && player.y < goal.y + goal.h && player.y + player.h > goal.y) { gameActive = false; alert("GOAL!!"); location.reload(); }
        ctx.fillStyle = "blue"; ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.restore();
        if(player.y > canvas.height) { gameActive = false; alert("落下しました..."); location.reload(); }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=450)
