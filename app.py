import streamlit as st
import random
import streamlit.components.v1 as components

# --- 数当てゲームの関数 ---
def number_guessing_game():
    st.header("🎮 数当てゲーム")

    # レベル選択
    level = st.radio("難易度を選んでね：", ["Level 1 (1-100)", "Level 2 (1-1000)"], horizontal=True)
    max_num = 100 if "Level 1" in level else 1000
    
    # セッション状態の初期化
    if 'target_number' not in st.session_state or st.session_state.get('current_max') != max_num:
        st.session_state.target_number = random.randint(1, max_num)
        st.session_state.current_max = max_num
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.last_guess = None

    # キャラクターの表情とメッセージを決めるロジック
    char_face = "👤"
    char_msg = f"1から{max_num}の間で数字を当ててみてね！"

    if st.session_state.game_over:
        char_face = "🎉"
        char_msg = f"レベル完了！正解は 【{st.session_state.target_number}】 だったね！おめでとう！"
    elif st.session_state.last_guess is not None:
        diff = abs(st.session_state.target_number - st.session_state.last_guess)
        
        if st.session_state.last_guess < st.session_state.target_number:
            hint = "もっと【大きい】よ！ ⬆️"
        else:
            hint = "もっと【小さい】よ！ ⬇️"

        if diff <= (max_num // 20):
            char_face = "😳"
            char_msg = f"【{st.session_state.last_guess}】は、めちゃくちゃ惜しい！ {hint}"
        elif st.session_state.attempts >= 10:
            char_face = "😰"
            char_msg = f"【{st.session_state.last_guess}】かぁ。{hint} 頑張って！"
        else:
            char_face = "😊"
            char_msg = f"【{st.session_state.last_guess}】だね。 {hint}"

    # キャラクターを表示
    with st.chat_message("assistant", avatar=char_face):
        st.markdown(f"### {char_msg}")
        st.write(f"難易度: {level} | 現在の挑戦回数: {st.session_state.attempts}回")

    # ユーザー入力
    user_guess = st.number_input(f"1〜{max_num}の数字を入力してEnterを押してね:", min_value=1, max_value=max_num, step=1, key="guess", value=None)

    # 数字が入力され、かつ前の入力と違う場合に判定
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

    # セッション状態の初期化
    if 'janken_wins' not in st.session_state:
        st.session_state.janken_wins = 0
    if 'janken_losses' not in st.session_state:
        st.session_state.janken_losses = 0
    if 'janken_draws' not in st.session_state:
        st.session_state.janken_draws = 0
    if 'janken_result' not in st.session_state:
        st.session_state.janken_result = None

    # 手の定義
    hands = {"グー": "✊", "チョキ": "✌️", "パー": "🖐️"}
    
    # ユーザーの手を選択
    cols = st.columns(3)
    user_hand = None
    if cols[0].button("✊ グー", use_container_width=True): user_hand = "グー"
    if cols[1].button("✌️ チョキ", use_container_width=True): user_hand = "チョキ"
    if cols[2].button("🖐️ パー", use_container_width=True): user_hand = "パー"

    if user_hand:
        cpu_hand = random.choice(list(hands.keys()))
        
        # 勝敗判定
        if user_hand == cpu_hand:
            result = "引き分け！"
            st.session_state.janken_draws += 1
            face = "😐"
        elif (user_hand == "グー" and cpu_hand == "チョキ") or \
             (user_hand == "チョキ" and cpu_hand == "パー") or \
             (user_hand == "パー" and cpu_hand == "グー"):
            result = "あなたの勝ち！"
            st.session_state.janken_wins += 1
            face = "😆"
            if st.session_state.janken_wins % 3 == 0: st.balloons()
        else:
            result = "あなたの負け..."
            st.session_state.janken_losses += 1
            face = "😭"
        
        st.session_state.janken_result = {
            "user": hands[user_hand],
            "cpu": hands[cpu_hand],
            "text": result,
            "face": face
        }

    # 結果表示
    if st.session_state.janken_result:
        res = st.session_state.janken_result
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; color: black;">
            <h1 style="font-size: 3em; margin: 0;">{res['user']} vs {res['cpu']}</h1>
            <h2 style="margin: 10px 0;">{res['face']} {res['text']}</h2>
        </div>
        """, unsafe_allow_html=True)

    # 戦績表示
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("勝ち", st.session_state.janken_wins)
    c2.metric("負け", st.session_state.janken_losses)
    c3.metric("引き分け", st.session_state.janken_draws)

    if st.button("戦績をリセット"):
        st.session_state.janken_wins = 0
        st.session_state.janken_losses = 0
        st.session_state.janken_draws = 0
        st.session_state.janken_result = None
        st.rerun()

# --- インベーダーゲームの関数 ---
def invader_game():
    st.header("👾 インベーダー・クエスト PRO")
    st.write("【スコアの掟】正確に、かつ速く殲滅せよ！")

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

    let score = 0;
    let shotsFired = 0;
    let enemiesDefeated = 0;
    let startTime = Date.now();
    let gameActive = true;

    const player = { x: 180, y: 370, w: 40, h: 20, speed: 5 };
    const bullets = [];
    const enemies = [];
    const enemyRows = 3;
    const enemyCols = 6;

    function initEnemies() {
        enemies.length = 0;
        for (let i = 0; i < enemyRows; i++) {
            for (let j = 0; j < enemyCols; j++) {
                enemies.push({ x: j * 50 + 50, y: i * 40 + 30, w: 30, h: 20, alive: true });
            }
        }
    }
    initEnemies();

    let rightPressed = false;
    let leftPressed = false;
    let spacePressed = false;

    window.addEventListener("keydown", (e) => {
        if(!gameActive) return;
        if(e.key == "Right" || e.key == "ArrowRight") rightPressed = true;
        if(e.key == "Left" || e.key == "ArrowLeft") leftPressed = true;
        if(e.key == " " || e.code == "Space") {
            if (!spacePressed) {
                bullets.push({ x: player.x + 18, y: player.y, r: 3, speed: 8 });
                shotsFired++;
                score = Math.max(0, score - 5); // 弾を撃つと少し減点
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

    let enemyDirection = 1;
    let enemyMoveCounter = 0;

    function calculateFinalScore() {
        let timeElapsed = (Date.now() - startTime) / 1000;
        let accuracy = shotsFired > 0 ? (enemiesDefeated / shotsFired) : 0;
        // 基本点 + 命中率ボーナス + タイムボーナス(最大1000)
        let timeBonus = Math.max(0, 1000 - Math.floor(timeElapsed * 10));
        let accuracyBonus = Math.floor(accuracy * 1000);
        return score + accuracyBonus + timeBonus;
    }

    function draw() {
        if(!gameActive) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let timeElapsed = (Date.now() - startTime) / 1000;
        timerElement.innerText = timeElapsed.toFixed(1);

        // プレイヤー
        ctx.fillStyle = "#00FF00";
        ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.fillRect(player.x + 15, player.y - 5, 10, 5);

        if(rightPressed && player.x < canvas.width - player.w) player.x += player.speed;
        if(leftPressed && player.x > 0) player.x -= player.speed;

        // 弾
        ctx.fillStyle = "yellow";
        for(let i = bullets.length - 1; i >= 0; i--) {
            let b = bullets[i];
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fill();
            b.y -= b.speed;
            if(b.y < 0) bullets.splice(i, 1);
        }

        // 敵
        let edgeReached = false;
        let aliveCount = 0;
        enemies.forEach(e => {
            if (!e.alive) return;
            aliveCount++;
            ctx.fillStyle = "red";
            ctx.fillRect(e.x, e.y, e.w, e.h);
            
            bullets.forEach((b, bIndex) => {
                if (b.x > e.x && b.x < e.x + e.w && b.y > e.y && b.y < e.y + e.h) {
                    e.alive = false;
                    bullets.splice(bIndex, 1);
                    enemiesDefeated++;
                    score += 100;
                    scoreElement.innerText = score;
                }
            });

            if (enemyMoveCounter > 25) {
                if (e.x + 10 * enemyDirection > canvas.width - e.w || e.x + 10 * enemyDirection < 0) edgeReached = true;
            }
        });

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

        if (enemies.some(e => e.alive && e.y > 350)) {
            gameActive = false;
            alert("GAME OVER! スコアが足りなかったようです...\\n最終スコア: " + score);
            location.reload();
        }

        if (aliveCount === 0) {
            gameActive = false;
            let final = calculateFinalScore();
            alert("MISSION COMPLETE!\\n\\n撃破点: " + score + "\\n命中率: " + Math.floor((enemiesDefeated/shotsFired)*100) + "%\\nタイム: " + timeElapsed.toFixed(1) + "秒\\n━━━━━━━━━━\\n最終スコア: " + final);
            location.reload();
        }

        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """
    components.html(game_html, height=550)

# --- メイン制御 ---
def main():
    st.set_page_config(page_title="My Game Center", page_icon="🕹️")
    
    st.sidebar.title("🕹️ Game Center")
    game_choice = st.sidebar.selectbox("遊ぶゲームを選んでね", ["数当てゲーム", "じゃんけんバトル", "インベーダーゲーム"])

    if game_choice == "数当てゲーム":
        number_guessing_game()
    elif game_choice == "じゃんけんバトル":
        janken_game()
    elif game_choice == "インベーダーゲーム":
        invader_game()

    # サイドバーに共通の設定
    st.sidebar.markdown("---")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
