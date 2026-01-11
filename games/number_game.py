import streamlit as st
import random

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
