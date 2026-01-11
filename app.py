import streamlit as st
import random

def main():
    st.set_page_config(page_title="数当てゲーム", page_icon="🎮")
    
    st.title("🎮 シンプル数当てゲーム")

    # レベル選択
    level = st.radio("難易度を選んでね：", ["Level 1 (1-100)", "Level 2 (1-1000)"], horizontal=True)
    max_num = 100 if "Level 1" in level else 1000
    
    # セッション状態の初期化
    # レベルが変更されたらリセットする仕組み
    if 'current_max' not in st.session_state or st.session_state.current_max != max_num:
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
        
        # ヒント（大きい・小さい）を決定
        if st.session_state.last_guess < st.session_state.target_number:
            hint = "もっと【大きい】よ！ ⬆️"
        else:
            hint = "もっと【小さい】よ！ ⬇️"

        if diff <= (max_num // 20): # レベルに応じて「惜しい」の基準を変える
            char_face = "😳"
            char_msg = f"【{st.session_state.last_guess}】は、めちゃくちゃ惜しい！ {hint}"
        else:
            char_face = "😊"
            char_msg = f"【{st.session_state.last_guess}】だね。 {hint}"

    # キャラクターを表示
    with st.chat_message("assistant", avatar=char_face):
        st.markdown(f"### {char_msg}")
        st.write(f"難易度: {level} | 現在の挑戦回数: {st.session_state.attempts}回")

    # ゲームのリセット
    def reset_game():
        st.session_state.target_number = random.randint(1, max_num)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.last_guess = None

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

    # もう一度遊ぶボタン
    if st.session_state.game_over:
        if st.button("もう一度遊ぶ"):
            reset_game()
            st.rerun()

    # サイドバー
    with st.sidebar:
        st.write("### 設定")
        if st.button("ゲームをリセット"):
            reset_game()
            st.rerun()

if __name__ == "__main__":
    main()
