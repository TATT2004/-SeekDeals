from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 爬蟲函數
def get_discounts(location):
    # 模擬爬取優惠食品的網站（範例 URL，可以換成實際便利商店的促銷頁面）
    url = f"https://familymap.pages.dev/friendly/a/407={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 假設優惠品在 HTML 的 class 'discount-item' 裡
    items = soup.find_all("div", class_="discount-item")
    results = []
    for item in items:
        name = item.find("h3").text
        price = item.find("span", class_="price").text
        expiry = item.find("span", class_="expiry").text
        results.append({"name": name, "price": price, "expiry": expiry})
    return results

# 路由：主頁
@app.route("/", methods=["GET", "POST"])
def index():
    discounts = []
    location = ""
    if request.method == "POST":
        location = request.form.get("location")
        discounts = get_discounts(location)
    return render_template("index.html", discounts=discounts, location=location)

if __name__ == "__main__":
    app.run(debug=True)
