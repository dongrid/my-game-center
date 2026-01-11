import streamlit as st
import random

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

# --- メイン制御 ---
def main():
    st.set_page_config(page_title="My Game Center", page_icon="🕹️")
    
    st.sidebar.title("🕹️ Game Center")
    game_choice = st.sidebar.selectbox("遊ぶゲームを選んでね", ["数当てゲーム", "じゃんけんバトル"])

    if game_choice == "数当てゲーム":
        number_guessing_game()
    elif game_choice == "じゃんけんバトル":
        janken_game()

    # サイドバーに共通の設定
    st.sidebar.markdown("---")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
