from flask import Flask, render_template, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

DB_FILE = 'db.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    return []

@app.route('/')
def index():
    data = load_db()
    images = []
    for entry in data:
        images.extend(entry['images'])
    return render_template('index.html', images=images)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
