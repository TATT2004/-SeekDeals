from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests, json, os
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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

def scrape_to_json_pizzahut(url, output_file):
    # 發送 HTTP 請求
    response = requests.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 範例：提取文章標題和連結
    data = []
    items = soup.find_all('div', class_='promotion_list_item')
    for item in items:
        img_tag = item.find('img')
        img_src = None
        if img_tag and hasattr(img_tag, 'get'):
            img_src = img_tag.get('data-original') or img_tag.get('src')
        titles = item.find('span', class_='pro-li-name')
        contents = item.find('p', class_='pro-list-desc')
        for img, title, content in zip(img_src, titles, contents):
            info = {
                'src': img_src,
                'title': title.get_text(),
                'content': content.get_text()
            }
            data.append(info)

    # 將資料寫入 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"資料已成功寫入 {output_file}！")

scrape_to_json_pizzahut('https://www.pizzahut.com.tw/promotions/?parent_id=2670', 'static/pizzahut/discounts.json')

def scrape_to_json_domino(url, output_file):
    # 創建 requests.Session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    })
    
    # 發送 HTTP 請求
    response = session.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取數據
    data = []
    items = soup.find_all('div', class_='col-12 col-md-6 col-lg-4 mt-3')  # 找到所有產品容器
    for item in items:
        img_tag = item.find('img', class_='img-fluid product-card-img w-100')
        img_src = img_tag.get('src') if img_tag else "No image"
        title_tag = item.find('h4', class_='product-title')
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        content_tags = item.find_all('li')
        content_list = [li.get_text(strip=True) for li in content_tags]
        store_tag = item.find('span', style="color:#3498db")
        stores = store_tag.get_text(strip=True).replace("◆ 適用門市:", "") if store_tag else "No store information"

        # 組裝數據
        info = {
            'src': img_src,
            'title': title,
            'content': content_list,
            'stores': stores
        }
        data.append(info)

    # 確保目錄存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 將資料寫入 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"資料已成功寫入 {output_file}！")

scrape_to_json_domino('https://www.dominos.com.tw/Alliances/Limited-20211206', 'static/domino/discounts.json')

def scrape_to_json_burgerking(url, output_file):
     # 發送 HTTP 請求
    response = requests.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 範例：提取文章標題和連結
    data = []
    items = soup.find_all('a', href=True)

    for item in items:
        img_container = item.find('div', class_='flex justify-center px-3')
        title_container = item.find('div', class_='md:px-0 md:px-10 md:text-xl px-2 text-center text-lg')
        content_container = item.find('div', class_='flex flex-wrap justify-center md:flex-nowrap mt-3')

        if img_container and title_container and content_container:
            img_tag = img_container.find('img')
            img_src = img_tag.get('src') if img_tag else "No image"
            title = title_container.get_text(strip=True)
            content = content_container.get_text(strip=True)
            info = {
                'src': img_src,
                'title': title,
                'content': content
            }
            data.append(info)

    # 將資料寫入 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"資料已成功寫入 {output_file}！")

scrape_to_json_burgerking('https://www.burgerking.com.tw/category/6', 'static/burgerking/discounts.json')

def scrape_to_json_subway(url, output_file):
    # 發送 HTTP 請求
    response = requests.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 範例：提取文章標題和連結
    data = []
    seen_titles = set()  # 用於跟蹤已處理的標題
    items = soup.find_all('div', class_='event-list')
    valid_items = [item for item in items if 'event-close' not in item.a.get('class', [])]
    for item in valid_items:
        img_tag = item.find('img', class_='img-fluid')
        img_src = img_tag.get('src') if img_tag else "No image"
        title_tag = item.find('h5')
        content_tag = item.find('p')
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        content = content_tag.get_text(strip=True) if content_tag else "No content"
        # 跳過重複的標題
        if title in seen_titles:
            continue
        seen_titles.add(title)  # 記錄標題

        # 組裝數據
        info = {
            'src': img_src,
            'title': title,
            'content': content
        }
        data.append(info)

    # 將資料寫入 JSON 檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"資料已成功寫入 {output_file}！")
    
scrape_to_json_subway('https://subway.com.tw/GoWeb2/include/index.php?Page=3', 'static/subway/discounts.json')

def scrape_to_json_tkk(url, output_file):
    # 發送 HTTP 請求
    response = requests.get(url)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 範例：提取文章標題和連結
    data = []
    items = soup.find_all('div', class_='announcement--content')
    for item in items:
        imgs = item.find_all('img')
        titles = item.find_all('h2')
        contents = item.find_all('p')
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

scrape_to_json_tkk('https://www.tkkinc.com.tw/event.html', 'static/tkk/discounts.json')

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

    session['user'] = {
        'username': username,
        **users[username]
    }
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

    users[username] =  {'password': password, 'logged': False , 'attention' : []}
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    # 註冊成功
    return jsonify({'message': '註冊成功！'}), 200

@app.route('/attention', methods=['POST'])
def attention():
    data = request.get_json()
    username = data.get('username')
    shop = data.get('shop')

    users = {}
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    attention_list = users[username]['attention']
    # 檢查是否已關注
    if shop in attention_list :
        return jsonify({'message': '此店家已關注'}), 400
    
    # 系統存取資料
    attention_list.append(shop)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    session['user'] = {
        'username': username,
        **users[username]
    }
    # 關注成功
    return jsonify({'message': '關注成功!', 'redirect': url_for('home')}), 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    username = data.get('username')
    shop = data.get('shop')

    users = {}
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    if shop not in users[username]['attention']:
        return jsonify({'message': '取消關注失敗'}), 400
    
    users[username]['attention'].remove(shop)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    session['user'] = {
        'username': username,
        **users[username]
    }
    return jsonify({'message': '取消關注成功!', 'redirect': url_for('home')}), 200

@app.route('/home')
def home():
    return render_template('home.html', user=session['user'])

@app.route('/store/mcdonal')
def mcdonal():
    data = {}
    with open('static/mcdonal/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/mcdonal.html', data=data)

@app.route('/store/kfc')
def kfc():
    data = {}
    with open('static/kfc/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/kfc.html', data=data)

@app.route('/store/pizzahut')
def pizzahut():
    data = {}
    with open('static/pizzahut/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/pizzahut.html', data=data)

@app.route('/store/domino')
def domino():
    data = {}
    with open('static/domino/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/domino.html', data=data)

@app.route('/store/burgerking')
def burgerking():
    data = {}
    with open('static/burgerking/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/burgerking.html', data=data)

@app.route('/store/subway')
def subway():
    data = {}
    with open('static/subway/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/subway.html', data=data)

@app.route('/store/tkk')
def tkk():
    data = {}
    with open('static/tkk/discounts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('store/tkk.html', data=data)

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
