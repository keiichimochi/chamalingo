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
    .review-card {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'wrong_phrases' not in st.session_state:
    st.session_state.wrong_phrases = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

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

def show_review():
    st.markdown("## 🔍 復習が必要な熟語")
    if len(st.session_state.wrong_phrases) == 0:
        st.success("🎉 全問正解！素晴らしいナリ！")
    else:
        for phrase in st.session_state.wrong_phrases:
            st.markdown(f"""
            <div class="review-card">
                <h3>🎯 {phrase['phrase']}</h3>
                <p><strong>意味:</strong> {phrase['meaning']}</p>
                <p><strong>例文:</strong> {phrase['example']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("もう一度チャレンジ！ 🔄"):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.wrong_phrases = []
        st.session_state.game_over = False
        st.session_state.current_phrase = None
        st.experimental_rerun()

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
    
    # ゲーム終了時のレビュー画面
    if st.session_state.game_over:
        show_review()
        return
    
    phrases = load_phrases()
    
    # 進捗バーの表示
    progress = st.session_state.question_count / 10
    st.progress(progress)
    st.markdown(f"### 問題 {st.session_state.question_count + 1}/10")
    
    # 新しい問題を生成
    if not st.session_state.current_phrase or st.session_state.answered:
        if st.session_state.question_count >= 10:
            st.session_state.game_over = True
            st.experimental_rerun()
            return
        st.session_state.current_phrase = random.choice(phrases)
        st.session_state.answered = False
        st.session_state.wrong_attempts = 0
    
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
                st.session_state.question_count += 1
            else:
                st.session_state.wrong_attempts += 1
                if st.session_state.wrong_attempts >= 3:
                    st.error("😢 3回間違えてしまったナリ...")
                    st.session_state.play_incorrect = True
                    st.info(f"""
                    ### 正解は: {st.session_state.current_phrase['meaning']} ナリ！
                    #### 例文: {st.session_state.current_phrase['example']}
                    """)
                    # 間違えた熟語を記録
                    if st.session_state.current_phrase not in st.session_state.wrong_phrases:
                        st.session_state.wrong_phrases.append(st.session_state.current_phrase)
                    st.session_state.answered = True
                    st.session_state.question_count += 1
                else:
                    st.error(f"😢 不正解... (残り{3 - st.session_state.wrong_attempts}回)")
                    st.session_state.play_incorrect = True
            
    # スコア表示
    st.sidebar.markdown(f"### スコア: {st.session_state.score}/10")
    
    # 次の問題へ
    if st.session_state.answered:
        if st.button("次の問題へ ➡️"):
            st.session_state.current_phrase = None
            st.experimental_rerun()

if __name__ == "__main__":
    main() 