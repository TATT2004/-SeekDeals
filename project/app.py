from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests, json, os
from bs4 import BeautifulSoup

app = Flask(__name__)
family_url = 'https://www.family.com.tw/Marketing/zh/Event#03'
mcdonal_url = 'https://www.mcdonalds.com/tw/zh-tw/whats-hot.html'

def scrape_to_json(url, output_file):
    # 發送 HTTP 請求
    response = requests.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 範例：提取文章標題和連結
    data = []
    items = soup.find_all('div', class_='cmp-container--three-col')
    for item in items:
        imgs = item.find_all('img', class_='cmp-image__image')
        titles = item.find_all('span', class_='heading-4')
        contents = item.find_all('div', class_='cmp-teaser__description')
        for img, title, content in zip(imgs, titles, contents):
            info = {
                'src': img.get('src'),
                'title': title.get_text(),
                'content': content.get_text()
            }
            data.append(info)

    # 將資料寫入 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"資料已成功寫入 {output_file}！")

scrape_to_json('https://www.mcdonalds.com/tw/zh-tw/whats-hot.html', 'static/mcdonal/discounts.json')

# 路由：主頁
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login/index')
def login_index():
    return render_template('login/index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = {}
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
                return jsonify({'message': '請註冊帳號'}), 400
    if username not in users:
        return jsonify({'message': '請註冊帳號'}), 400
    
    if password != users[username]['password']:
        return jsonify({'message': '請正確輸入帳號與密碼'}), 400
    
    users[username]['logged'] = True
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    return jsonify({'message': '登入成功', 'redirect': url_for('home')}), 200

@app.route('/register/index')
def register_index():
    return render_template('register/index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = {}
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    if username in users:
        return jsonify({'message': '帳號已存在'}), 400

    users[username] =  {'password': password, 'logged': False}
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    # 註冊成功
    return jsonify({'message': '註冊成功！'}), 200

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/store/mcdonal')
def mcdonal():
    data = {}
    with open('static/mcdonal/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/mcdonal.html', data=data)

if __name__ == "__main__":
    users = {}
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
    for user in users:
        users[user]['logged'] = False
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    app.run(debug=True)
