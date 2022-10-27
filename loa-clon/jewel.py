from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By

client = MongoClient('mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.loagg

app = Flask(__name__)


@app.route('/')
def search():
    return render_template('search.html')


@app.route('/main')
def main():
    return render_template('main.html')


# search에서 name 받아오기
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

            doc['gemImgList'].append(a)  # gemImgList[num]

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
                # profile-jewel > div > div.jewel-effect__list > div > ul > li.active > span > img
                # profile-jewel > div > div.jewel-effect__list > div > ul > li:nth-child(2) > span > img
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

            doc['skillImg'].append(a)  # gemImgList[num]
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

        # 카드-재하----------------------------------------------------------------------
        cardlist = [soup.select_one('#cardList > li:nth-child(1)'),
                    soup.select_one('#cardList > li:nth-child(2)'),
                    soup.select_one('#cardList > li:nth-child(3)'),
                    soup.select_one('#cardList > li:nth-child(4)'),
                    soup.select_one('#cardList > li:nth-child(5)'),
                    soup.select_one('#cardList > li:nth-child(6)'), ]

        cardimglist = []
        cardnamelist = []
        cardawakelist = []

        cardsetlist = [soup.select_one('#cardSetList > li:nth-child(1)'),
                       soup.select_one('#cardSetList > li:nth-child(2)'),
                       soup.select_one('#cardSetList > li:nth-child(3)'),
                       soup.select_one('#cardSetList > li:nth-child(4)'),
                       soup.select_one('#cardSetList > li:nth-child(5)'),
                       soup.select_one('#cardSetList > li:nth-child(6)'), ]
        cardsettitlelist = []
        cardsetdsclist = []

        for card in cardlist:
            cardname = card.select_one('div > strong > font').text
            cardnamelist.append(cardname)
            cardimg = card.select_one('div > img')['src']
            cardimglist.append(cardimg)
            cardawake = card.select_one('div')['data-awake']
            cardawakelist.append(cardawake)
            doc = {
                'name': name,
                'cardname': cardnamelist,
                'cardimg': cardimglist,
                'cardawake': cardawakelist
            };
            db.cardlist.update_one({"name": name}, {'$set': doc}, upsert=True)

        for cardset in cardsetlist:
            if cardset is not None:
                cardsettitle = cardset.select_one('div.card-effect__title').text
                cardsettitlelist.append(cardsettitle)
                cardsetdsc = cardset.select_one('div.card-effect__dsc').text
                cardsetdsclist.append(cardsetdsc)
                doc = {
                    'name': name,
                    'cardsettitle': cardsettitlelist,
                    'cardsetdsc': cardsetdsclist
                }
                db.cardsetlist.update_one({"name": name}, {'$set': doc}, upsert=True)

        # 스텟-덕현-----------------------------------------------------------------------------

        # 공격력
        Power = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(2)').text
        PowerNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        PowerNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        # 최대 생명력
        Life = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > span:nth-child(2)').text
        LifeNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > div > ul > li:nth-child(2) > textformat > textformat > font:nth-child(2)').text
        LifeNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        # 치명
        Critical = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > span:nth-child(2)').text
        CriticalNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        CriticalNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        # 특화
        Specialization = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > span:nth-child(2)').text
        SpecializationNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        SpecializationNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        SpecializationNumer3 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        SpecializationNumer4 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text
        SpecializationNumer5 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(5) > textformat > font:nth-child(2)').text

        # 제압
        Domination = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)').text
        DominationNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        DominationNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        DominationNumer3 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        # 신속
        Swiftness = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > span:nth-child(2)').text
        SwiftnessNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        SwiftnessNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        SwiftnessNumer3 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        SwiftnessNumer4 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text

        # 인내
        Endurance = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)').text
        EnduranceNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        EnduranceNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        EnduranceNumer3 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        EnduranceNumer4 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text
        EnduranceNumer5 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(5) > textformat > font:nth-child(2)').text
        # 숙련
        Expertise = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)').text
        ExpertiseNumer1 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
        ExpertiseNumer2 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
        ExpertiseNumer3 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
        ExpertiseNumer4 = soup.select_one(
            '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text

        # 각인효과 리스트화
        Engravelist = soup.select_one('#profile-ability > div.profile-ability-engrave > div > div.swiper-wrapper').text
        Engrave = Engravelist.split('\n')
        Engrave = list(filter(None, Engrave))

        doc = {
            'Power': Power,
            'Life': Life,
            'Critical': Critical,
            'Specialization': Specialization,
            'Domination': Domination,
            'Swiftness': Swiftness,
            'Endurance': Endurance,
            'Expertise': Expertise
        }
        db.AbilityStats.update_one({"name": name}, {'$set': doc}, upsert=True)

        doc = {
            'PowerNumer1': PowerNumer1,
            'PowerNumer2': PowerNumer2,
            'LifeNumer1': LifeNumer1,
            'LifeNumer2': LifeNumer2,
            'CriticalNumer1': CriticalNumer1,
            'CriticalNumer2': CriticalNumer2,
            'SpecializationNumer1': SpecializationNumer1,
            'SpecializationNumer2': SpecializationNumer2,
            'SpecializationNumer3': SpecializationNumer3,
            'SpecializationNumer4': SpecializationNumer4,
            'SpecializationNumer5': SpecializationNumer5,
            'DominationNumer1': DominationNumer1,
            'DominationNumer2': DominationNumer2,
            'DominationNumer3': DominationNumer3,
            'SwiftnessNumer1': SwiftnessNumer1,
            'SwiftnessNumer2': SwiftnessNumer2,
            'SwiftnessNumer3': SwiftnessNumer3,
            'SwiftnessNumer4': SwiftnessNumer4,
            'EnduranceNumer1': EnduranceNumer1,
            'EnduranceNumer2': EnduranceNumer2,
            'EnduranceNumer3': EnduranceNumer3,
            'EnduranceNumer4': EnduranceNumer4,
            'EnduranceNumer5': EnduranceNumer5,
            'ExpertiseNumer1': ExpertiseNumer1,
            'ExpertiseNumer2': ExpertiseNumer2,
            'ExpertiseNumer3': ExpertiseNumer3,
            'ExpertiseNumer4': ExpertiseNumer4
        }
        db.AbilityStatsTooltip.update_one({"name": name}, {'$set': doc}, upsert=True)

        doc = {
            'Engrave': Engrave
        }
        db.Engrave.update_one({"name": name}, {'$set': doc}, upsert=True)

        return jsonify({'msg': 'suc'})

# GET ----------------------------------------------------------------------------------------------------------------------------------------

@app.route("/api/jewels", methods=["GET"])
def jewels_get():
    jewels_get = db.gemInfoList.find_one({'name': f'{name}'}, {'_id': False})

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


# 재하 카드 ------------------------------------------------------------------------------------------------------------------------------------
@app.route("/card", methods=['GET'])
def card():
    cardlist = db.cardlist.find_one({'name': f'{name}'}, {'_id': False})
    card_img = cardlist['cardimg']
    card_name = cardlist['cardname']
    card_awake = cardlist['cardawake']

    return jsonify({'card_img': card_img, 'card_name': card_name, 'card_awake': card_awake})


@app.route("/cardset", methods=['GET'])
def cardset():
    cardsetlist = db.cardsetlist.find_one({'name': f'{name}'}, {'_id': False})
    cardset_title = cardsetlist['cardsettitle']
    cardset_dsc = cardsetlist['cardsetdsc']

    return jsonify({'cardset_title': cardset_title, 'cardset_dsc': cardset_dsc})


# 덕현 스텟 -------------------------------------------------------------------------------------------------------------------------------------
@app.route("/ability", methods=['GET'])
def ability():
    abilityStats = db.AbilityStats.find_one({'name': f'{name}'}, {'_id': False})
    abilityStatTooltips = db.AbilityStatsTooltip.find_one({'name': f'{name}'}, {'_id': False})
    engrave = db.Engrave.find_one({'name': f'{name}'}, {'_id': False})
    engraveList = engrave['Engrave']

    return jsonify({'abilityStats': abilityStats, 'abilityStatTooltips': abilityStatTooltips, 'engraveList': engraveList})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
