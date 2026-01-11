import streamlit as st
import random
import streamlit.components.v1 as components

# --- 数当てゲームの関数 ---
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

    char_face = "👤"
    char_msg = f"1から{max_num}の間で数字を当ててみてね！"

    if st.session_state.game_over:
        char_face = "🎉"
        char_msg = f"レベル完了！正解は 【{st.session_state.target_number}】 だったね！おめでとう！"
    elif st.session_state.last_guess is not None:
        diff = abs(st.session_state.target_number - st.session_state.last_guess)
        hint = "もっと【大きい】よ！ ⬆️" if st.session_state.last_guess < st.session_state.target_number else "もっと【小さい】よ！ ⬇️"
        if diff <= (max_num // 20):
            char_face = "😳"
            char_msg = f"【{st.session_state.last_guess}】は、めちゃくちゃ惜しい！ {hint}"
        elif st.session_state.attempts >= 10:
            char_face = "😰"
            char_msg = f"【{st.session_state.last_guess}】かぁ。{hint} 頑張って！"
        else:
            char_face = "😊"
            char_msg = f"【{st.session_state.last_guess}】だね。 {hint}"

    with st.chat_message("assistant", avatar=char_face):
        st.markdown(f"### {char_msg}")
        st.write(f"難易度: {level} | 現在の挑戦回数: {st.session_state.attempts}回")

    user_guess = st.number_input(f"1〜{max_num}の数字を入力してEnterを押してね:", min_value=1, max_value=max_num, step=1, key="guess", value=None)

    if user_guess is not None and user_guess != st.session_state.last_guess and not st.session_state.game_over:
        st.session_state.last_guess = user_guess
        st.session_state.attempts += 1
        if user_guess == st.session_state.target_number:
            st.session_state.game_over = True
            st.balloons()
        st.rerun()

    if st.session_state.game_over:
        if st.button("もう一度遊ぶ"):
            st.session_state.target_number = random.randint(1, max_num)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.session_state.last_guess = None
            st.rerun()

# --- じゃんけんゲームの関数 ---
def janken_game():
    st.header("✊ じゃんけんバトル")
    st.write("CPUと対戦！3回勝つとバルーンが飛ぶよ！")

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
        if user_hand == cpu_hand:
            result, face = "引き分け！", "😐"
            st.session_state.janken_draws += 1
        elif (user_hand == "グー" and cpu_hand == "チョキ") or (user_hand == "チョキ" and cpu_hand == "パー") or (user_hand == "パー" and cpu_hand == "グー"):
            result, face = "あなたの勝ち！", "😆"
            st.session_state.janken_wins += 1
            if st.session_state.janken_wins % 3 == 0: st.balloons()
        else:
            result, face = "あなたの負け...", "😭"
            st.session_state.janken_losses += 1
        st.session_state.janken_result = {"user": hands[user_hand], "cpu": hands[cpu_hand], "text": result, "face": face}

    if st.session_state.janken_result:
        res = st.session_state.janken_result
        st.markdown(f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; color: black;'><h1 style='font-size: 3em; margin: 0;'>{res['user']} vs {res['cpu']}</h1><h2 style='margin: 10px 0;'>{res['face']} {res['text']}</h2></div>", unsafe_allow_html=True)

    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("勝ち", st.session_state.janken_wins)
    c2.metric("負け", st.session_state.janken_losses)
    c3.metric("引き分け", st.session_state.janken_draws)

# --- インベーダーゲームの関数 ---
def invader_game():
    st.header("👾 インベーダー・クエスト PRO")
    st.write("左右キーで移動、スペースキーで発射！")
    game_html = """
    <div id="game-container" style="text-align: center; background: #1a1a1a; padding: 15px; border-radius: 15px; border: 2px solid #333;">
        <canvas id="gameCanvas" width="400" height="400" style="background: black; border: 1px solid #444; cursor: crosshair;"></canvas>
        <div style="display: flex; justify-content: space-around; color: #00FF00; font-family: 'Courier New', monospace; margin-top: 15px; background: #000; padding: 10px; border-radius: 5px;">
            <div>SCORE: <span id="score">0</span></div>
            <div>SHOTS: <span id="shots">0</span></div>
            <div>TIME: <span id="timer">0.0</span>s</div>
        </div>
    </div>
    <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const scoreElement = document.getElementById('score');
    const shotsElement = document.getElementById('shots');
    const timerElement = document.getElementById('timer');
    let score = 0, shotsFired = 0, enemiesDefeated = 0, startTime = Date.now(), gameActive = true;
    const player = { x: 180, y: 370, w: 40, h: 20, speed: 5 }, bullets = [], enemies = [];
    function initEnemies() {
        enemies.length = 0;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 6; j++) enemies.push({ x: j * 50 + 50, y: i * 40 + 30, w: 30, h: 20, alive: true });
        }
    }
    initEnemies();
    let rightPressed = false, leftPressed = false, spacePressed = false;
    window.addEventListener("keydown", (e) => {
        if(!gameActive) return;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
        if(e.key == " " || e.code == "Space") {
            if (!spacePressed) { bullets.push({ x: player.x + 18, y: player.y, r: 3, speed: 8 }); shotsFired++; score = Math.max(0, score - 5); shotsElement.innerText = shotsFired; }
            spacePressed = true; e.preventDefault();
        }
    });
    window.addEventListener("keyup", (e) => {
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        if(e.key == " ") spacePressed = false;
    });
    let enemyDirection = 1, enemyMoveCounter = 0;
    function calculateFinalScore() {
        let timeElapsed = (Date.now() - startTime) / 1000;
        let accuracy = shotsFired > 0 ? (enemiesDefeated / shotsFired) : 0;
        let timeBonus = Math.max(0, 1000 - Math.floor(timeElapsed * 10));
        let accuracyBonus = Math.floor(accuracy * 1000);
        return score + accuracyBonus + timeBonus;
    }
    function draw() {
        if(!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let timeElapsed = (Date.now() - startTime) / 1000;
        timerElement.innerText = timeElapsed.toFixed(1);
        ctx.fillStyle = "#00FF00";
        ctx.fillRect(player.x, player.y, player.w, player.h);
        if(rightPressed && player.x < canvas.width - player.w) player.x += player.speed;
        if(leftPressed && player.x > 0) player.x -= player.speed;
        ctx.fillStyle = "yellow";
        for(let i = bullets.length - 1; i >= 0; i--) {
            let b = bullets[i]; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2); ctx.fill();
            b.y -= b.speed; if(b.y < 0) bullets.splice(i, 1);
        }
        let edgeReached = false, aliveCount = 0;
        enemies.forEach(e => {
            if (!e.alive) return;
            aliveCount++; ctx.fillStyle = "red"; ctx.fillRect(e.x, e.y, e.w, e.h);
            bullets.forEach((b, bIndex) => {
                if (b.x > e.x && b.x < e.x + e.w && b.y > e.y && b.y < e.y + e.h) {
                    e.alive = false; bullets.splice(bIndex, 1); enemiesDefeated++; score += 100; scoreElement.innerText = score;
                }
            });
            if (enemyMoveCounter > 25) { if (e.x + 10 * enemyDirection > canvas.width - e.w || e.x + 10 * enemyDirection < 0) edgeReached = true; }
        });
        if (enemyMoveCounter > 25) {
            if (edgeReached) { enemyDirection *= -1; enemies.forEach(e => e.y += 20); } else { enemies.forEach(e => e.x += 10 * enemyDirection); }
            enemyMoveCounter = 0;
        }
        enemyMoveCounter++;
        if (enemies.some(e => e.alive && e.y > 350)) { gameActive = false; alert("GAME OVER!"); location.reload(); }
        if (aliveCount === 0) { gameActive = false; alert("MISSION COMPLETE! Score: " + calculateFinalScore()); location.reload(); }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=550)

# --- クローン・ゲートの関数 ---
def clone_gate_game():
    st.header("👥 クローン・ゲート")
    st.write("左右キーで移動！ゲートを通って軍勢を増やし、敵の城（100人）を攻略せよ！")

    game_html = """
    <div id="game-container" style="text-align: center; background: #222; padding: 15px; border-radius: 15px;">
        <canvas id="gateCanvas" width="400" height="500" style="background: #eee; border: 3px solid #333;"></canvas>
        <div style="color: white; font-family: sans-serif; margin-top: 10px; font-size: 24px; font-weight: bold;">
            SOLDIERS: <span id="count">1</span>
        </div>
    </div>
    <script>
    const canvas = document.getElementById('gateCanvas');
    const ctx = canvas.getContext('2d');
    const countElement = document.getElementById('count');
    let soldiers = 1, playerX = 180, distance = 0, gameActive = true;
    const goalDistance = 2500, gates = [];
    function createGates() {
        for(let i = 1; i < 8; i++) {
            let y = -i * 350;
            let leftType = Math.random() > 0.5 ? 'add' : 'mul';
            let leftVal = leftType === 'add' ? Math.floor(Math.random() * 10) + 5 : 2;
            gates.push({ x: 0, y: y, w: 200, h: 40, type: leftType, val: leftVal, text: (leftType==='add'?'+':'x')+leftVal, color: '#3b82f6' });
            let rightType = Math.random() > 0.7 ? 'sub' : 'add';
            let rightVal = rightType === 'sub' ? Math.floor(Math.random() * 10) + 1 : Math.floor(Math.random() * 5) + 1;
            gates.push({ x: 200, y: y, w: 200, h: 40, type: rightType, val: rightVal, text: (rightType==='sub'?'-':'+')+rightVal, color: rightType==='sub'?'#ef4444':'#3b82f6' });
        }
    }
    createGates();
    let leftPressed = false, rightPressed = false;
    window.addEventListener("keydown", (e) => {
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
    });
    window.addEventListener("keyup", (e) => {
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = false;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = false;
    });
    function draw() {
        if(!gameActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ddd"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        distance += 4;
        ctx.fillStyle = "#3b82f6";
        for(let i = 0; i < Math.min(soldiers, 60); i++) {
            let offsetX = (i % 6) * 7 - 15; let offsetY = Math.floor(i / 6) * 7;
            ctx.beginPath(); ctx.arc(playerX + 20 + offsetX, 450 - offsetY, 3, 0, Math.PI*2); ctx.fill();
        }
        if(leftPressed && playerX > 0) playerX -= 6;
        if(rightPressed && playerX < canvas.width - 40) playerX += 6;
        gates.forEach((g, index) => {
            let currentY = g.y + distance;
            if(currentY > -100 && currentY < 600) {
                ctx.fillStyle = g.color; ctx.globalAlpha = 0.6; ctx.fillRect(g.x, currentY, g.w, g.h);
                ctx.globalAlpha = 1.0; ctx.fillStyle = "white"; ctx.font = "bold 20px Arial"; ctx.fillText(g.text, g.x + 80, currentY + 28);
                if(currentY > 410 && currentY < 450 && playerX + 20 > g.x && playerX + 20 < g.x + g.w) {
                    if(g.type === 'add') soldiers += g.val; else if(g.type === 'mul') soldiers *= g.val; else if(g.type === 'sub') soldiers = Math.max(1, soldiers - g.val);
                    countElement.innerText = soldiers; gates.splice(index, 1);
                }
            }
        });
        if(distance > goalDistance) {
            gameActive = false; let enemyCount = 100;
            if(soldiers >= enemyCount) alert("VICTORY! 軍勢: " + soldiers + " vs 敵: " + enemyCount);
            else alert("DEFEAT... 軍勢: " + soldiers + " vs 敵: " + enemyCount);
            location.reload();
        }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=600)

# --- メイン制御 ---
def main():
    st.set_page_config(page_title="My Game Center", page_icon="🕹️")
    st.sidebar.title("🕹️ Game Center")
    game_choice = st.sidebar.selectbox("遊ぶゲームを選んでね", ["数当てゲーム", "じゃんけんバトル", "インベーダーゲーム", "クローン・ゲート"])
    if game_choice == "数当てゲーム": number_guessing_game()
    elif game_choice == "じゃんけんバトル": janken_game()
    elif game_choice == "インベーダーゲーム": invader_game()
    elif game_choice == "クローン・ゲート": clone_gate_game()
    st.sidebar.markdown("---")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
