from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.loagg

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/main')
def main():
    return render_template('main.html')

#search에서 name 받아오기
@app.route("/api/names", methods=["POST"])
def save_name():
    global name
    name = request.form['name_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/{name}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    gem00_img = soup.select_one("#gem00 > span.jewel_img > img")['src']
    gem01_img = soup.select_one("#gem01 > span.jewel_img > img")['src']
    gem02_img = soup.select_one("#gem02 > span.jewel_img > img")['src']
    gem03_img = soup.select_one("#gem03 > span.jewel_img > img")['src']
    gem04_img = soup.select_one("#gem04 > span.jewel_img > img")['src']
    gem05_img = soup.select_one("#gem05 > span.jewel_img > img")['src']
    gem06_img = soup.select_one("#gem06 > span.jewel_img > img")['src']
    gem07_img = soup.select_one("#gem07 > span.jewel_img > img")['src']
    gem08_img = soup.select_one("#gem08 > span.jewel_img > img")['src']
    gem09_img = soup.select_one("#gem09 > span.jewel_img > img")['src']
    gem10_img = soup.select_one("#gem10 > span.jewel_img > img")['src']

    gem00_lv = soup.select_one('#gem00 > span.jewel_level').text
    gem01_lv = soup.select_one('#gem01 > span.jewel_level').text
    gem02_lv = soup.select_one('#gem02 > span.jewel_level').text
    gem03_lv = soup.select_one('#gem03 > span.jewel_level').text
    gem04_lv = soup.select_one('#gem04 > span.jewel_level').text
    gem05_lv = soup.select_one('#gem05 > span.jewel_level').text
    gem06_lv = soup.select_one('#gem06 > span.jewel_level').text
    gem07_lv = soup.select_one('#gem07 > span.jewel_level').text
    gem08_lv = soup.select_one('#gem08 > span.jewel_level').text
    gem09_lv = soup.select_one('#gem09 > span.jewel_level').text
    gem10_lv = soup.select_one('#gem00 > span.jewel_level').text

    doc = {
        #캐릭터명
        'name': name,

        #보석 이미지
        'gem00_img': gem00_img,
        'gem01_img': gem01_img,
        'gem02_img': gem02_img,
        'gem03_img': gem03_img,
        'gem04_img': gem04_img,
        'gem05_img': gem05_img,
        'gem06_img': gem06_img,
        'gem07_img': gem07_img,
        'gem08_img': gem08_img,
        'gem09_img': gem09_img,
        'gem10_img': gem10_img,

        #보석 레벨
        'gem00_lv': gem00_lv,
        'gem01_lv': gem01_lv,
        'gem02_lv': gem02_lv,
        'gem03_lv': gem03_lv,
        'gem04_lv': gem04_lv,
        'gem05_lv': gem05_lv,
        'gem06_lv': gem06_lv,
        'gem07_lv': gem07_lv,
        'gem08_lv': gem08_lv,
        'gem09_lv': gem09_lv,
        'gem10_lv': gem10_lv,
    }

    db.jewel.update_one({"name": f'{name}'}, {'$set': doc}, upsert=True);

    return ""

@app.route("/api/jewels", methods=["GET"])
def bucket_get():
    jewel_get = db.jewel.find_one({'name':f'{name}'}, {'_id': False})

    return jsonify({'jewel': jewel_get})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)