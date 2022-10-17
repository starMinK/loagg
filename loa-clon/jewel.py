from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

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
@app.route("/api/save-info", methods=["POST"])
def save_jewels():
    global name
    name = request.form['name_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/{name}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    is_exist_name = soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')

    if is_exist_name is None:
        return jsonify({'msg': f'{name} 캐릭터 정보가 없습니다.\n캐릭터명을 확인해주세요.'})
    else:
        isGemExistList = [soup.select_one('#gem00'),
                          soup.select_one('#gem01'),
                          soup.select_one('#gem02'),
                          soup.select_one('#gem03'),
                          soup.select_one('#gem04'),
                          soup.select_one('#gem05'),
                          soup.select_one('#gem06'),
                          soup.select_one('#gem07'),
                          soup.select_one('#gem08'),
                          soup.select_one('#gem09'),
                          soup.select_one('#gem10')]

        gemImgList = []
        gemLvList = []

        num = 0
        for a in isGemExistList:
            numStr = str(num)
            if a is not None:
                gemImg = soup.select_one(f'#gem{numStr.zfill(2)} > span.jewel_img > img')
                gemImgList.append(gemImg['src'])

                gemLv = soup.select_one(f'#gem{numStr.zfill(2)} > span.jewel_level')
                gemLvList.append(gemLv.text)

            num = num + 1

        doc = {}
        doc['gemImgList'] = []
        doc['gemLvList'] = []

        num = 0
        for a in gemImgList:
            numStr = str(num)

            doc['gemImgList'].append(a) #gemImgList[num]

            doc['gemLvList'].append(gemLvList[num])

            num += 1

        db.gemInfoList.update_one({"name": f'{name}'}, {'$set': doc}, upsert=True)

        skillImgList = []
        skillNameList = []
        skillEffectList = []

        num = 1
        for a in isGemExistList:
            if a is not None:
                skillImg = soup.select_one(
                    f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > span > img')
                skillImgList.append(skillImg['src'])

                skillName = soup.select_one(
                    f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > strong')
                skillNameList.append(skillName.text)

                skillEffect = soup.select_one(
                    (f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > p'))
                skillEffectList.append(skillEffect.text)
            num += 1

        doc = {}
        doc['skillImg'] = []
        doc['skillName'] = []
        doc['skillEffect'] = []

        num = 0
        for a in skillImgList:
            numStr = str(num)

            doc['skillImg'].append(a) # gemImgList[num]
            doc['skillName'].append(skillNameList[num])
            doc['skillEffect'].append(skillEffectList[num])

            num += 1

        db.gemSkillList.update_one({"name": f'{name}'}, {'$set': doc}, upsert=True)
    return jsonify({'msg': 'suc'})

@app.route("/api/jewels", methods=["GET"])
def jewels_get():
    jewels_get = db.gemInfoList.find_one({'name':f'{name}'}, {'_id': False})

    jewels_img = jewels_get['gemImgList']
    jewels_lv = jewels_get['gemLvList']


    return jsonify({'jewels_img': jewels_img, 'jewels_lv': jewels_lv})


@app.route("/api/gem-skills", methods=["GET"])
def skills_get():
    skill_get = db.gemSkillList.find_one({'name':f'{name}'}, {'_id': False})

    skills_img = skill_get['skillImg']
    skills_name = skill_get['skillName']
    skills_effect = skill_get['skillEffect']



    return jsonify({'skills_img': skills_img, 'skills_name': skills_name, 'skills_effect': skills_effect})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)