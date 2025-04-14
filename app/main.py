from flask import Flask, request, jsonify
import os
import json
from pathlib import Path

app = Flask(__name__)

WELCOME_MSG = os.getenv('WELCOME_MSG', 'Welcome to the custom app')
LOG_FILE = os.getenv('LOG_FILE', '/app/logs/app.log')

Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)


@app.route('/')
def home():
    return WELCOME_MSG


@app.route('/status')
def status():
    return jsonify({"status": "ok"})


@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(data) + '\n')
    return jsonify({"status": "logged"}), 201


@app.route('/logs')
def logs():
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
        return jsonify({"logs": logs})
    except FileNotFoundError:
        return jsonify({"logs": []})


@app.route('/id')
def id():
    return os.getenv('HOSTNAME')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
