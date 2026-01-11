import streamlit as st
import random
import streamlit.components.v1 as components

# --- ページ設定 ---
st.set_page_config(page_title="My Game Center", page_icon="🕹️", layout="centered")

# --- 数当てゲーム ---
def number_guessing_game():
    st.header("🎮 数当てゲーム")
    level = st.radio("難易度を選んでね：", ["Level 1 (1-100)", "Level 2 (1-1000)"], horizontal=True)
    max_num = 100 if "Level 1" in level else 1000
    if 'target_number' not in st.session_state or st.session_state.get('current_max') != max_num:
        st.session_state.target_number = random.randint(1, max_num)
        st.session_state.current_max = max_num
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.last_guess = None
    char_face, char_msg = "👤", f"1から{max_num}の間で数字を当ててみてね！"
    if st.session_state.game_over:
        char_face, char_msg = "🎉", f"レベル完了！正解は 【{st.session_state.target_number}】 だったね！おめでとう！"
    elif st.session_state.last_guess is not None:
        diff = abs(st.session_state.target_number - st.session_state.last_guess)
        hint = "もっと【大きい】よ！ ⬆️" if st.session_state.last_guess < st.session_state.target_number else "もっと【小さい】よ！ ⬇️"
        if diff <= (max_num // 20): char_face, char_msg = "😳", f"【{st.session_state.last_guess}】は、めちゃくちゃ惜しい！ {hint}"
        else: char_face, char_msg = "😊", f"【{st.session_state.last_guess}】だね。 {hint}"
    with st.chat_message("assistant", avatar=char_face):
        st.markdown(f"### {char_msg}")
        st.write(f"現在の挑戦回数: {st.session_state.attempts}回")
    user_guess = st.number_input(f"1〜{max_num}の数字を入力してEnterを押してね:", min_value=1, max_value=max_num, step=1, key="guess", value=None)
    if user_guess is not None and user_guess != st.session_state.last_guess and not st.session_state.game_over:
        st.session_state.last_guess = user_guess
        st.session_state.attempts += 1
        if user_guess == st.session_state.target_number:
            st.session_state.game_over = True
            st.balloons()
        st.rerun()
    if st.session_state.game_over and st.button("もう一度遊ぶ"):
        st.session_state.target_number = random.randint(1, max_num); st.session_state.attempts = 0
        st.session_state.game_over = False; st.session_state.last_guess = None; st.rerun()

# --- じゃんけんゲーム ---
def janken_game():
    st.header("✊ じゃんけんバトル")
    if 'janken_wins' not in st.session_state: st.session_state.janken_wins = 0
    if 'janken_losses' not in st.session_state: st.session_state.janken_losses = 0
    if 'janken_draws' not in st.session_state: st.session_state.janken_draws = 0
    if 'janken_result' not in st.session_state: st.session_state.janken_result = None
    hands = {"グー": "✊", "チョキ": "✌️", "パー": "🖐️"}
    cols = st.columns(3)
    user_hand = None
    if cols[0].button("✊ グー", use_container_width=True): user_hand = "グー"
    if cols[1].button("✌️ チョキ", use_container_width=True): user_hand = "チョキ"
    if cols[2].button("🖐️ パー", use_container_width=True): user_hand = "パー"
    if user_hand:
        cpu_hand = random.choice(list(hands.keys()))
        if user_hand == cpu_hand: result, face, st.session_state.janken_draws = "引き分け！", "😐", st.session_state.janken_draws + 1
        elif (user_hand == "グー" and cpu_hand == "チョキ") or (user_hand == "チョキ" and cpu_hand == "パー") or (user_hand == "パー" and cpu_hand == "グー"):
            result, face, st.session_state.janken_wins = "あなたの勝ち！", "😆", st.session_state.janken_wins + 1
            if st.session_state.janken_wins % 3 == 0: st.balloons()
        else: result, face, st.session_state.janken_losses = "あなたの負け...", "😭", st.session_state.janken_losses + 1
        st.session_state.janken_result = {"user": hands[user_hand], "cpu": hands[cpu_hand], "text": result, "face": face}
    if st.session_state.janken_result:
        res = st.session_state.janken_result
        st.markdown(f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; color: black;'><h1 style='font-size: 3em; margin: 0;'>{res['user']} vs {res['cpu']}</h1><h2 style='margin: 10px 0;'>{res['face']} {res['text']}</h2></div>", unsafe_allow_html=True)
    st.write("---")
    c1, c2, c3 = st.columns(3); c1.metric("勝ち", st.session_state.janken_wins); c2.metric("負け", st.session_state.janken_losses); c3.metric("引き分け", st.session_state.janken_draws)

# --- インベーダーゲーム ---
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
    const canvas = document.getElementById('gameCanvas'); const ctx = canvas.getContext('2d');
    const scoreElement = document.getElementById('score'); const shotsElement = document.getElementById('shots'); const timerElement = document.getElementById('timer');
    let score = 0, shotsFired = 0, enemiesDefeated = 0, startTime = Date.now(), gameActive = true;
    const player = { x: 180, y: 370, w: 40, h: 20, speed: 5 }, bullets = [], enemies = [];
    function initEnemies() { for (let i = 0; i < 3; i++) for (let j = 0; j < 6; j++) enemies.push({ x: j * 50 + 50, y: i * 40 + 30, w: 30, h: 20, alive: true }); }
    initEnemies();
    let rightPressed = false, leftPressed = false, spacePressed = false;
    window.addEventListener("keydown", (e) => {
        if(!gameActive) return;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true; if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
        if(e.key == " " || e.code == "Space") { if (!spacePressed) { bullets.push({ x: player.x + 18, y: player.y, r: 3, speed: 8 }); shotsFired++; score = Math.max(0, score - 5); shotsElement.innerText = shotsFired; } spacePressed = true; e.preventDefault(); }
    });
    window.addEventListener("keyup", (e) => { if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false; if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false; if(e.key == " ") spacePressed = false; });
    let enemyDirection = 1, enemyMoveCounter = 0;
    function calculateFinalScore() {
        let timeElapsed = (Date.now() - startTime) / 1000;
        let accuracy = shotsFired > 0 ? (enemiesDefeated / shotsFired) : 0;
        let timeBonus = Math.max(0, 1000 - Math.floor(timeElapsed * 10));
        let accuracyBonus = Math.floor(accuracy * 1000);
        return score + accuracyBonus + timeBonus;
    }
    function draw() {
        if(!gameActive) return; ctx.clearRect(0, 0, canvas.width, canvas.height);
        let timeElapsed = (Date.now() - startTime) / 1000; timerElement.innerText = timeElapsed.toFixed(1);
        ctx.fillStyle = "#00FF00"; ctx.fillRect(player.x, player.y, player.w, player.h);
        if(rightPressed && player.x < canvas.width - player.w) player.x += player.speed; if(leftPressed && player.x > 0) player.x -= player.speed;
        ctx.fillStyle = "yellow"; for(let i = bullets.length - 1; i >= 0; i--) { let b = bullets[i]; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2); ctx.fill(); b.y -= b.speed; if(b.y < 0) bullets.splice(i, 1); }
        let edgeReached = false, aliveCount = 0;
        enemies.forEach(e => {
            if (!e.alive) return; aliveCount++; ctx.fillStyle = "red"; ctx.fillRect(e.x, e.y, e.w, e.h);
            bullets.forEach((b, bIndex) => { if (b.x > e.x && b.x < e.x + e.w && b.y > e.y && b.y < e.y + e.h) { e.alive = false; bullets.splice(bIndex, 1); enemiesDefeated++; score += 100; scoreElement.innerText = score; } });
            if (enemyMoveCounter > 25) { if (e.x + 10 * enemyDirection > canvas.width - e.w || e.x + 10 * enemyDirection < 0) edgeReached = true; }
        });
        if (enemyMoveCounter > 25) { if (edgeReached) { enemyDirection *= -1; enemies.forEach(e => e.y += 20); } else { enemies.forEach(e => e.x += 10 * enemyDirection); } enemyMoveCounter = 0; }
        enemyMoveCounter++;
        if (enemies.some(e => e.alive && e.y > 350)) { gameActive = false; alert("GAME OVER!"); location.reload(); }
        if (aliveCount === 0) { gameActive = false; alert("MISSION COMPLETE! Score: " + calculateFinalScore()); location.reload(); }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=550)

# --- クローン・シュート ---
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

# --- 横スクロールアクション ---
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

# --- レーシングゲーム ---
def racing_game():
    st.header("🏎️ マリオカート風レーシング")
    st.write("左右キーでハンドル操作！ライバル車を避けてコインを集め、パワーアップをゲットせよ！")
    game_html = """
    <div id="game-container" style="text-align: center; background: #333; padding: 15px; border-radius: 15px;">
        <canvas id="raceCanvas" width="500" height="600" style="background: #87CEEB; border: 3px solid #555; cursor: pointer;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('raceCanvas'); const ctx = canvas.getContext('2d');
    let gameActive = false, gameStarted = false, frameCount = 0;
    let score = 0, speed = 6, distance = 0, playerLane = 1;
    const lanes = [100, 200, 300, 400];
    const player = { x: lanes[1], y: 500, w: 50, h: 80, lane: 1 };
    const enemies = [], coins = [], powerups = [];
    
    function createEnemy() {
        let lane = Math.floor(Math.random() * 4);
        enemies.push({ x: lanes[lane], y: -150, w: 50, h: 80, lane: lane, speed: Math.random() * 2 + 3 });
    }
    function createCoin() {
        let lane = Math.floor(Math.random() * 4);
        coins.push({ x: lanes[lane] + 25, y: -50, r: 15, lane: lane });
    }
    function createPowerup() {
        let lane = Math.floor(Math.random() * 4);
        powerups.push({ x: lanes[lane] + 25, y: -50, r: 20, lane: lane, type: Math.random() > 0.5 ? 'speed' : 'shield' });
    }
    
    let keys = {}, lastKey = null;
    function startGame() { if(!gameStarted) { gameStarted = true; gameActive = true; } }
    window.addEventListener("keydown", e => { 
        startGame(); 
        if(e.code === "ArrowRight" && lastKey !== "ArrowRight" && playerLane < 3) { playerLane++; lastKey = "ArrowRight"; }
        if(e.code === "ArrowLeft" && lastKey !== "ArrowLeft" && playerLane > 0) { playerLane--; lastKey = "ArrowLeft"; }
        if(["ArrowLeft","ArrowRight","Space"].includes(e.code)) e.preventDefault(); 
    });
    window.addEventListener("keyup", e => { if(e.code === "ArrowLeft" || e.code === "ArrowRight") lastKey = null; });
    canvas.addEventListener('click', startGame);
    
    function drawRoad() {
        ctx.fillStyle = "#555";
        ctx.fillRect(50, 0, 400, canvas.height);
        ctx.strokeStyle = "yellow"; ctx.setLineDash([30, 30]); ctx.lineDashOffset = -distance;
        ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(canvas.width/2, 0); ctx.lineTo(canvas.width/2, canvas.height); ctx.stroke();
        ctx.setLineDash([]);
        ctx.strokeStyle = "white"; ctx.lineWidth = 2;
        for(let i = 0; i < 4; i++) {
            ctx.beginPath(); ctx.moveTo(50 + (i * 100), 0); ctx.lineTo(50 + (i * 100), canvas.height); ctx.stroke();
        }
    }
    
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#654321"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        drawRoad();
        
        if(!gameStarted) {
            ctx.fillStyle = "rgba(0,0,0,0.6)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white"; ctx.font = "bold 30px Arial"; ctx.textAlign = "center";
            ctx.fillText("🏎️ RACING GAME", canvas.width/2, canvas.height/2 - 20);
            ctx.font = "18px Arial"; ctx.fillText("CLICK or PRESS ANY KEY", canvas.width/2, canvas.height/2 + 30);
            requestAnimationFrame(draw); return;
        }
        if(!gameActive) return;
        
        frameCount++; distance += speed;
        if(frameCount % 80 === 0) createEnemy();
        if(frameCount % 120 === 0) createCoin();
        if(frameCount % 200 === 0) createPowerup();
        speed = 6 + Math.floor(score / 500);
        
        player.x += (lanes[playerLane] - player.x) * 0.2;
        
        ctx.fillStyle = "red";
        for(let i = enemies.length - 1; i >= 0; i--) {
            let e = enemies[i]; e.y += speed;
            ctx.fillRect(e.x, e.y, e.w, e.h);
            ctx.fillStyle = "darkred"; ctx.fillRect(e.x + 5, e.y + 10, 40, 20);
            ctx.fillStyle = "red";
            if(player.x < e.x + e.w && player.x + player.w > e.x && player.y < e.y + e.h && player.y + player.h > e.y) {
                gameActive = false; alert("クラッシュ！ SCORE: " + score); location.reload();
            }
            if(e.y > canvas.height) enemies.splice(i, 1);
        }
        
        ctx.fillStyle = "gold";
        for(let i = coins.length - 1; i >= 0; i--) {
            let c = coins[i]; c.y += speed;
            ctx.beginPath(); ctx.arc(c.x, c.y, c.r, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "yellow"; ctx.beginPath(); ctx.arc(c.x, c.y, c.r - 3, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "gold";
            if(Math.hypot(player.x + 25 - c.x, player.y + 40 - c.y) < 35) { score += 50; coins.splice(i, 1); }
            if(c.y > canvas.height) coins.splice(i, 1);
        }
        
        ctx.fillStyle = "purple";
        for(let i = powerups.length - 1; i >= 0; i--) {
            let p = powerups[i]; p.y += speed;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "white"; ctx.font = "bold 16px Arial"; ctx.textAlign = "center";
            ctx.fillText(p.type === 'speed' ? '⚡' : '🛡️', p.x, p.y + 5);
            ctx.fillStyle = "purple";
            if(Math.hypot(player.x + 25 - p.x, player.y + 40 - p.y) < 40) {
                if(p.type === 'speed') { speed += 2; score += 200; }
                else { score += 300; }
                powerups.splice(i, 1);
            }
            if(p.y > canvas.height) powerups.splice(i, 1);
        }
        
        ctx.fillStyle = "blue"; ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.fillStyle = "lightblue"; ctx.fillRect(player.x + 8, player.y + 15, 34, 25);
        ctx.fillStyle = "white"; ctx.font = "bold 20px Arial"; ctx.textAlign = "left";
        ctx.fillText("SCORE: " + score, 10, 30);
        ctx.fillText("SPEED: " + (speed * 15) + "km/h", 10, 60);
        ctx.fillText("DISTANCE: " + Math.floor(distance / 10) + "m", 10, 90);
        
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=650)

# --- メイン制御 ---
def main():
    st.title("🕹️ My Game Center")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎮 数当て", "✊ じゃんけん", "👾 インベーダー", "👥 クローン", "🏃 ランナー", "🏎️ レース"])
    with tab1: number_guessing_game()
    with tab2: janken_game()
    with tab3: invader_game()
    with tab4: clone_shoot_game()
    with tab5: side_scroller_game()
    with tab6: racing_game()
    st.sidebar.title("⚙️ 設定")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
