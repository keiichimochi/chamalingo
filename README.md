# 🦎 Chamalingo

Duolingo風の楽しい英熟語学習アプリナリ！

## 🌟 特徴

- 🎮 ゲーミフィケーションで楽しく学習
- 🎯 4択クイズ形式で効率的に覚える
- 🎨 美しいアニメーションとエフェクト
- 🔊 効果音でモチベーションアップ
- 📊 スコア管理機能

## 🚀 セットアップ

1. 仮想環境を作成して有効化:
```bash
uv venv
source .venv/bin/activate  # Linuxの場合
.venv\Scripts\activate  # Windowsの場合
```

2. 依存パッケージをインストール:
```bash
uv pip install -r requirements.txt
```

3. アプリを起動:
```bash
streamlit run app.py
```

## 🎯 使い方

1. アプリを起動すると、ランダムな英熟語が表示されます
2. 4つの選択肢から正しい意味を選んでください
3. 正解するとスコアが加算され、派手なエフェクトが表示されます
4. 「次の問題へ」ボタンで次の問題に進めます

## 🛠️ 技術スタック

- Python 3.9+
- Streamlit
- Streamlit-Lottie (アニメーション)
- Playsound (効果音) 