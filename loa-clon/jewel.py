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


    isGemImgExistList = [soup.select_one("#gem00 > span.jewel_img > img"),
                      soup.select_one("#gem01> span.jewel_img > img"),
                      soup.select_one("#gem02 > span.jewel_img > img"),
                      soup.select_one("#gem03 > span.jewel_img > img"),
                      soup.select_one("#gem04 > span.jewel_img > img"),
                      soup.select_one("#gem05 > span.jewel_img > img"),
                      soup.select_one("#gem06 > span.jewel_img > img"),
                      soup.select_one("#gem07 > span.jewel_img > img"),
                      soup.select_one("#gem08 > span.jewel_img > img"),
                      soup.select_one("#gem09 > span.jewel_img > img"),
                      soup.select_one("#gem10 > span.jewel_img > img")]

    isGemLvExistList = [soup.select_one(f'#gem00 > span.jewel_level'),
                        soup.select_one(f'#gem01 > span.jewel_level'),
                        soup.select_one(f'#gem02 > span.jewel_level'),
                        soup.select_one(f'#gem03 > span.jewel_level'),
                        soup.select_one(f'#gem04 > span.jewel_level'),
                        soup.select_one(f'#gem05 > span.jewel_level'),
                        soup.select_one(f'#gem06 > span.jewel_level'),
                        soup.select_one(f'#gem07 > span.jewel_level'),
                        soup.select_one(f'#gem08 > span.jewel_level'),
                        soup.select_one(f'#gem09 > span.jewel_level'),
                        soup.select_one(f'#gem10 > span.jewel_level')]

    gemImgList = []
    gemLvList = []


    for a in isGemImgExistList:
        if a is not None:
            gemImgList.append(a['src'])
        else:
            gemImgList.append('none')


    for a in isGemLvExistList:
        if a is not None:
            gemLvList.append(a.text)
        else:
            gemLvList.append("none")

    doc = {
        # 캐릭터명
        'name': name,

        # 보석 이미지
        'gem00_img': gemImgList[0],
        'gem01_img': gemImgList[1],
        'gem02_img': gemImgList[2],
        'gem03_img': gemImgList[3],
        'gem04_img': gemImgList[4],
        'gem05_img': gemImgList[5],
        'gem06_img': gemImgList[6],
        'gem07_img': gemImgList[7],
        'gem08_img': gemImgList[8],
        'gem09_img': gemImgList[9],
        'gem10_img': gemImgList[10],

        # 보석 레벨
        'gem00_lv': gemLvList[0],
        'gem01_lv': gemLvList[1],
        'gem02_lv': gemLvList[2],
        'gem03_lv': gemLvList[3],
        'gem04_lv': gemLvList[4],
        'gem05_lv': gemLvList[5],
        'gem06_lv': gemLvList[6],
        'gem07_lv': gemLvList[7],
        'gem08_lv': gemLvList[8],
        'gem09_lv': gemLvList[9],
        'gem10_lv': gemLvList[10],
    }

    db.jewel.update_one({"name": f'{name}'}, {'$set': doc}, upsert=True);
    return ""

@app.route("/api/jewels", methods=["GET"])
def bucket_get():
    jewel_get = db.jewel.find_one({'name':f'{name}'}, {'_id': False})

    return jsonify({'jewel': jewel_get})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)