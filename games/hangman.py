import streamlit as st
import random

def hangman_game():
    st.header("🎯 ハングマン")
    st.write("アルファベットを選んで、隠された単語を当てよう！")

    # 単語リスト（英単語）
    words = ["COMPUTER", "PROGRAMMING", "STREAMLIT", "GAME", "PYTHON", 
             "JAVASCRIPT", "APPLICATION", "INTERNET", "ALGORITHM", "DATABASE",
             "REACT", "NODEJS", "HTML", "CSS", "ANGULAR", "VUE", "DOCKER", "KUBERNETES"]

    # セッション状態の初期化
    if 'hangman_word' not in st.session_state:
        st.session_state.hangman_word = random.choice(words)
        st.session_state.hangman_guessed = set()
        st.session_state.hangman_wrong = 0
        st.session_state.hangman_game_over = False
        st.session_state.hangman_won = False
        st.session_state.hangman_last_input = ""

    word = st.session_state.hangman_word
    guessed = st.session_state.hangman_guessed
    wrong = st.session_state.hangman_wrong
    max_wrong = 6

    # 表示用の単語（当てた文字とアンダースコア）
    display_word = ""
    for char in word:
        if char in guessed:
            display_word += char + " "
        else:
            display_word += "_ "
    
    # 大文字小文字を区別せずに判定
    word_upper = word.upper()

    # ゲーム状態の判定
    if set(word_upper) <= guessed:
        st.session_state.hangman_won = True
        st.session_state.hangman_game_over = True
    elif wrong >= max_wrong:
        st.session_state.hangman_game_over = True

    # ハングマンの絵を表示
    hangman_stages = [
        "",
        "  O",
        "  O\n  |",
        "  O\n /|",
        "  O\n /|\\",
        "  O\n /|\\\n /",
        "  O\n /|\\\n / \\"
    ]
    
    st.code(hangman_stages[wrong], language="text")
    
    # 単語表示
    st.markdown(f"### {display_word}")
    st.write(f"間違い: {wrong}/{max_wrong}")

    # ゲームオーバー時の表示
    if st.session_state.hangman_game_over:
        if st.session_state.hangman_won:
            st.success(f"🎉 おめでとう！正解は「{word}」でした！")
            st.balloons()
        else:
            st.error(f"ゲームオーバー... 正解は「{word}」でした")
        
        if st.button("もう一度遊ぶ"):
            st.session_state.hangman_word = random.choice(words)
            st.session_state.hangman_guessed = set()
            st.session_state.hangman_wrong = 0
            st.session_state.hangman_game_over = False
            st.session_state.hangman_won = False
            st.session_state.hangman_last_input = ""
            st.rerun()
    else:
        # キーボード入力用のテキスト入力
        st.write("### 文字を選んでね")
        col1, col2 = st.columns([3, 1])
        with col1:
            key_input = st.text_input("キーボードでアルファベットを入力（Enterで確定）", 
                                     key="hangman_keyboard_input", 
                                     max_chars=1,
                                     placeholder="A-Zを入力",
                                     label_visibility="collapsed")
        with col2:
            st.write("")  # スペーサー
            st.write("または下のボタンをクリック")
        
        # キーボード入力の処理（前回の入力と異なる場合のみ）
        if key_input and key_input.upper() != st.session_state.hangman_last_input:
            char = key_input.upper()
            if char.isalpha() and len(char) == 1 and 'A' <= char <= 'Z':
                if char not in guessed:
                    st.session_state.hangman_guessed.add(char)
                    if char not in word_upper:
                        st.session_state.hangman_wrong += 1
                    # 前回の入力を記録
                    st.session_state.hangman_last_input = char
                    st.rerun()
        
        st.write("---")
        
        # アルファベット（A-Z）
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # 6列×5行でボタンを配置
        cols_per_row = 6
        for row in range(0, len(alphabet), cols_per_row):
            cols = st.columns(cols_per_row)
            for i, char in enumerate(alphabet[row:row+cols_per_row]):
                with cols[i]:
                    if st.button(char, key=f"hangman_{char}", disabled=char in guessed):
                        # 押した文字は必ずguessedに追加（正解・不正解に関わらず）
                        st.session_state.hangman_guessed.add(char)
                        if char in word_upper:
                            # 正解の場合は何もしない（既にguessedに追加済み）
                            pass
                        else:
                            # 間違いの場合はカウントを増やす
                            st.session_state.hangman_wrong += 1
                        st.rerun()
