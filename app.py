import streamlit as st
from games import number_game, janken, invader, clone_shoot, runner, racing

# --- ページ設定 ---
st.set_page_config(page_title="My Game Center", page_icon="🕹️", layout="centered")

# --- メイン制御 ---
def main():
    st.title("🕹️ My Game Center")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎮 数当て", "✊ じゃんけん", "👾 インベーダー", "👥 クローン", "🏃 ランナー", "🏎️ レース"])
    
    with tab1:
        number_game.number_guessing_game()
    with tab2:
        janken.janken_game()
    with tab3:
        invader.invader_game()
    with tab4:
        clone_shoot.clone_shoot_game()
    with tab5:
        runner.side_scroller_game()
    with tab6:
        racing.racing_game()
    
    st.sidebar.title("⚙️ 設定")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
