from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    #crowling
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/{name}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    #selenium
    url = f'https://lostark.game.onstove.com/Profile/Character/{name}'
    browser = webdriver.Chrome()
    browser.get(url)


    is_exist_name = soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')

    if is_exist_name is None:
        return jsonify({'msg': f'{name} 캐릭터 정보가 없습니다.\n캐릭터명을 확인해주세요.'})
    else:
        #gem 존재 여부 확인 list
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


        #존재하는 만큼 들어가는 list
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

######

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

######

        doc = {}
        doc['gemTooltipName'] = []
        doc['gemTooltipTear'] = []
        doc['gemTooltipEffect'] = []

        num = 0
        for a in isGemExistList:
            numStr = str(num)
            if a is not None:
                # 보석창 진입
                browser.find_element(By.XPATH, '//*[@id="profile-ability"]/div[1]/div[1]/a[3]').click()
                #보석 Tooltip창 hover
                browser.find_element(By.XPATH, f'//*[@id="gem{numStr.zfill(2)}"]').click()

                # 보석 이름
                gemTooltipName = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[1]/p/font').text
                doc['gemTooltipName'].append(gemTooltipName)
                # 보석 티어
                gemTooltipTear = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[2]/span[4]/font').text
                doc['gemTooltipTear'].append(gemTooltipTear)
                # 보석 효과
                if gemTooltipName.find('(귀속)') >= 0:
                    gemTooltipEffect = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[6]').text
                else:
                    gemTooltipEffect = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[5]').text

                doc['gemTooltipEffect'].append(gemTooltipEffect.replace("효과\n", ""))
                # //*[@id="lostark-wrapper"]/div[2]/div[6]

                num += 1
    db.gemTooltipList.update_one({"name": f'{name}'}, {'$set': doc}, upsert=True)

    return jsonify({'msg': 'suc'})

@app.route("/api/jewels", methods=["GET"])
def jewels_get():
    jewels_get = db.gemInfoList.find_one({'name':f'{name}'}, {'_id': False})

    jewels_img = jewels_get['gemImgList']
    jewels_lv = jewels_get['gemLvList']


    return jsonify({'jewels_img': jewels_img, 'jewels_lv': jewels_lv})


@app.route("/api/gem-skills", methods=["GET"])
def gemSkillsGet():
    gemSkillGet = db.gemSkillList.find_one({'name':f'{name}'}, {'_id': False})

    skillsImg = gemSkillGet['skillImg']
    skillsName = gemSkillGet['skillName']
    skillsEffect = gemSkillGet['skillEffect']



    return jsonify({'skillsImg': skillsImg, 'skillsName': skillsName, 'skillsEffect': skillsEffect})

@app.route("/api/gem-tooltips", methods=["GET"])
def gem_tooltips_get():
    gemTooltipGet = db.gemTooltipList.find_one({'name': f'{name}'}, {'_id': False})

    gemTooltipName = gemTooltipGet['gemTooltipName']
    gemTooltipTear = gemTooltipGet['gemTooltipTear']
    gemTooltipEffect = gemTooltipGet['gemTooltipEffect']

    return jsonify({'gemTooltipName': gemTooltipName, 'gemTooltipTear': gemTooltipTear, 'gemTooltipEffect': gemTooltipEffect})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)