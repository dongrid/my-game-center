import streamlit as st
from games import number_game, janken, invader, clone_shoot, runner, racing, hangman

# --- ページ設定 ---
st.set_page_config(page_title="My Game Center", page_icon="🕹️", layout="centered")

# --- メイン制御 ---
def main():
    st.title("🕹️ My Game Center")
    
    # ゲームリスト（追加・削除が簡単に）
    games = [
        ("🎮 数当て", number_game.number_guessing_game),
        ("✊ じゃんけん", janken.janken_game),
        ("👾 インベーダー", invader.invader_game),
        ("👥 クローン", clone_shoot.clone_shoot_game),
        ("🏃 ランナー", runner.side_scroller_game),
        ("🏎️ レース", racing.racing_game),
        ("🎯 ハングマン", hangman.hangman_game),
    ]
    
    # タブ名のリスト
    tab_names = [name for name, _ in games]
    tabs = st.tabs(tab_names)
    
    # 各タブでゲームを実行
    for tab, (_, game_func) in zip(tabs, games):
        with tab:
            game_func()
    
    st.sidebar.title("⚙️ 設定")
    if st.sidebar.button("全データをリセット"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
