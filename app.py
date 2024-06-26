from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.getenv('LINE_USER_ID')
APP_PASSWORD = os.getenv('APP_PASSWORD')

def load_menu():
    df = pd.read_csv('menu.csv')
    categories = df.groupby("category")["item"].apply(list).to_dict()
    return categories

@app.route('/')
def password():
    return render_template('password.html')

@app.route('/check-password', methods=['POST'])
def check_password():
    input_password = request.form.get('password')
    if input_password == APP_PASSWORD:
        session['authenticated'] = True
        return redirect(url_for('index'))
    else:
        return redirect(url_for('password'))

@app.route('/menu')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('password'))
    categories = load_menu()
    return render_template('index.html', categories=categories)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    #print(LINE_CHANNEL_ACCESS_TOKEN)
    menu_item = data.get('menuItem')
    print(menu_item)
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        'message': f'{menu_item}が選ばれました。'
    }
    response = requests.post(url, headers=headers, data=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)