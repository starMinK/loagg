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
@app.route("/api/save-info", methods=["POST"])
def save_jewels():
    global name
    name = request.form['name_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/{name}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

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

    isSkilExistList = [soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(1)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(2)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(3)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(4)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(5)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(6)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(7)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(8)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(9)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(10)'),
                       soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(11)')];



    num = 0
    for a in isGemExistList:
        numStr = str(num)
        if a is not None:
            gemImg = soup.select_one(f'#gem{numStr.zfill(2)} > span.jewel_img > img')
            gemImgList.append(gemImg['src'])
            gemLv = soup.select_one(f'#gem{numStr.zfill(2)} > span.jewel_level')
            gemLvList.append(gemLv.text)
        else:
            gemImgList.append('none')
            gemLvList.append("none")
        num = num + 1

    # for a in isSkilExistList:
    #     if a is not None:


    gem_doc = {
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

    isSkillExistList = [soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(1)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(2)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(3)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(4)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(5)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(6)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(7)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(8)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(9)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(10)'),
                        soup.select_one('#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(11)')]

    skillImgList = []
    skillNameList = []
    skillEffectList = []

    num = 1
    for a in isSkillExistList:
        if a is not None:
            # profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(1) > span > img
            skillImg = soup.select_one(
                f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > span > img')
            skillImgList.append(skillImg['src'])
            # profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(1) > strong
            skillName = soup.select_one(
                f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > strong')
            skillNameList.append(skillName.text)
            # profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(1) > p
            skillEffect = soup.select_one(
                (f'#profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child({str(num)}) > p'))
            skillEffectList.append(skillEffect.text)
        else:
            skillImgList.append("none")
            skillNameList.append("none")
            skillEffectList.append("none")
        num += 1

    skill_doc = {
        'name': name,

        'skillImg00': skillImgList[0],
        'skillImg01': skillImgList[1],
        'skillImg02': skillImgList[2],
        'skillImg03': skillImgList[3],
        'skillImg04': skillImgList[4],
        'skillImg05': skillImgList[5],
        'skillImg06': skillImgList[6],
        'skillImg07': skillImgList[7],
        'skillImg08': skillImgList[8],
        'skillImg09': skillImgList[9],
        'skillImg10': skillImgList[10],

        'skillName00': skillNameList[0],
        'skillName01': skillNameList[1],
        'skillName02': skillNameList[2],
        'skillName03': skillNameList[3],
        'skillName04': skillNameList[4],
        'skillName05': skillNameList[5],
        'skillName06': skillNameList[6],
        'skillName07': skillNameList[7],
        'skillName08': skillNameList[8],
        'skillName09': skillNameList[9],
        'skillName10': skillNameList[10],

        'skillEffect00': skillEffectList[0],
        'skillEffect01': skillEffectList[1],
        'skillEffect02': skillEffectList[2],
        'skillEffect03': skillEffectList[3],
        'skillEffect04': skillEffectList[4],
        'skillEffect05': skillEffectList[5],
        'skillEffect06': skillEffectList[6],
        'skillEffect07': skillEffectList[7],
        'skillEffect08': skillEffectList[8],
        'skillEffect09': skillEffectList[9],
        'skillEffect10': skillEffectList[10]
    }

    is_exist_name = soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')

    if is_exist_name is None:
        return jsonify({'msg': f'{name} 캐릭터 정보가 없습니다.\n캐릭터명을 확인해주세요.'})
    else:
        db.jewel.update_one({"name": f'{name}'}, {'$set': gem_doc}, upsert=True)
        db.gem_skills.update_one({"name": f'{name}'}, {'$set': skill_doc}, upsert=True)
        return jsonify({'msg': 'suc'})

@app.route("/api/jewels", methods=["GET"])
def jewels_get():
    jewel_get = db.jewel.find_one({'name':f'{name}'}, {'_id': False})

    return jsonify({'jewel': jewel_get})


@app.route("/api/gem-skills", methods=["GET"])
def skills_get():
    skill_get = db.gem_skills.find_one({'name':f'{name}'}, {'_id': False})

    return jsonify({'gem_skills': skill_get})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)