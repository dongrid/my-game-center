import streamlit as st
import random

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
