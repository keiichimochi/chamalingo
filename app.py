import os
import json
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_123"

# Load idioms data
def load_idioms_from_txt():
    try:
        with open('英検準１級熟語.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            return data
    except Exception as e:
        print(f"Error loading idioms from txt: {e}")
        return {"idioms": []}

idioms_data = load_idioms_from_txt()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/idioms')
def get_idioms():
    return jsonify(idioms_data)

@app.route('/static/sounds/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/sounds', filename)
