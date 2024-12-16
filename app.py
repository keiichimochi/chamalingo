import streamlit as st
import pandas as pd
import json
import random
import os
import requests
from streamlit_lottie import st_lottie

# ページ設定
st.set_page_config(
    page_title="Chamalingo - 楽しく英熟語を学ぼう！",
    page_icon="🦎",
    layout="centered"
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #45a049;
    }
    .question-text {
        font-size: 24px;
        color: #333;
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    audio {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# 効果音のHTML
correct_audio = """
<audio id="correct-sound" autoplay>
    <source src="assets/correct1.mp3" type="audio/mpeg">
</audio>
"""

incorrect_audio = """
<audio id="incorrect-sound" autoplay>
    <source src="assets/bomb.mp3" type="audio/mpeg">
</audio>
"""

# Lottieアニメーションを読み込む関数
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 正解時のアニメーション
lottie_correct = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# セッション状態の初期化
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_phrase' not in st.session_state:
    st.session_state.current_phrase = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'wrong_attempts' not in st.session_state:
    st.session_state.wrong_attempts = 0
if 'play_correct' not in st.session_state:
    st.session_state.play_correct = False
if 'play_incorrect' not in st.session_state:
    st.session_state.play_incorrect = False

# データの読み込み
def load_phrases():
    with open('words1s.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        phrases_data = []
        for phrase_block in content.split('- **熟語:**')[1:]:
            lines = phrase_block.strip().split('\n')
            phrase = lines[0].strip()
            meaning = lines[1].split('**意味:**')[1].strip()
            example = lines[2].split('**例文:**')[1].strip()
            phrases_data.append({
                'phrase': phrase,
                'meaning': meaning,
                'example': example
            })
    return phrases_data

# メインアプリ
def main():
    st.title("🦎 Chamalingo")
    st.subheader("楽しく英熟語を学ぼう！")
    
    # 効果音の再生
    if st.session_state.play_correct:
        st.markdown(correct_audio, unsafe_allow_html=True)
        st.session_state.play_correct = False
    if st.session_state.play_incorrect:
        st.markdown(incorrect_audio, unsafe_allow_html=True)
        st.session_state.play_incorrect = False
    
    phrases = load_phrases()
    
    # 新しい問題を生成
    if not st.session_state.current_phrase or st.session_state.answered:
        st.session_state.current_phrase = random.choice(phrases)
        st.session_state.answered = False
        st.session_state.wrong_attempts = 0  # 新しい問題が始まったらリセット
    
    # 問題表示
    st.markdown(f"""
    <div class='question-text'>
        <h2>この英熟語の意味は？</h2>
        <h3>{st.session_state.current_phrase['phrase']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 選択肢を生成（正解と3つのダミー）
    choices = [st.session_state.current_phrase['meaning']]
    while len(choices) < 4:
        dummy = random.choice(phrases)['meaning']
        if dummy not in choices:
            choices.append(dummy)
    random.shuffle(choices)
    
    # ボタンを表示
    for choice in choices:
        if st.button(choice):
            if choice == st.session_state.current_phrase['meaning']:
                st.success("🎉 正解！")
                st.session_state.score += 1
                st_lottie(lottie_correct, height=200, key="correct")
                st.session_state.play_correct = True
                st.session_state.answered = True
            else:
                st.session_state.wrong_attempts += 1
                if st.session_state.wrong_attempts >= 3:
                    st.error("😢 3回間違えてしまったナリ...")
                    st.session_state.play_incorrect = True
                    st.info(f"""
                    ### 正解は: {st.session_state.current_phrase['meaning']} ナリ！
                    #### 例文: {st.session_state.current_phrase['example']}
                    """)
                    st.session_state.answered = True
                else:
                    st.error(f"😢 不正解... (残り{3 - st.session_state.wrong_attempts}回)")
                    st.session_state.play_incorrect = True
            
    # スコア表示
    st.sidebar.markdown(f"### スコア: {st.session_state.score}")
    
    # 次の問題へ
    if st.session_state.answered:
        if st.button("次の問題へ ➡️"):
            st.session_state.current_phrase = None
            st.experimental_rerun()

if __name__ == "__main__":
    main() 