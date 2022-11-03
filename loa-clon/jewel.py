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
        try:
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
            PowerNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            PowerNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            # 최대 생명력
            Life = soup.select_one(
                '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > span:nth-child(2)').text
            LifeNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > div > ul > li:nth-child(2) > textformat > textformat > font:nth-child(2)').text
            LifeNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-basic > ul > li:nth-child(2) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            # 치명
            Critical = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > span:nth-child(2)').text
            CriticalNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            CriticalNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            # 특화
            Specialization = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > span:nth-child(2)').text
            SpecializationNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            SpecializationNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            SpecializationNumber3 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            SpecializationNumber4 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text
            SpecializationNumber5 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > div > ul > li:nth-child(5) > textformat > font:nth-child(2)')
            if SpecializationNumber5 is not None:
                SpecializationNumber5 = SpecializationNumber5.text
            else:
                SpecializationNumber5 = "0"

            # 제압
            Domination = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)').text
            DominationNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            DominationNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            DominationNumber3 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)')
            if DominationNumber3 is not None:
                DominationNumber3 = DominationNumber3.text
            else:
                DominationNumber3 = "0"

            # 신속
            Swiftness = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > span:nth-child(2)').text
            SwiftnessNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            SwiftnessNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            SwiftnessNumber3 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            SwiftnessNumber4 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)')
            if SwiftnessNumber4 is not None:
                SwiftnessNumber4 = SwiftnessNumber4.text
            else:
                SwiftnessNumber4 = "0"

            # 인내
            Endurance = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)').text
            EnduranceNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            EnduranceNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            EnduranceNumber3 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            EnduranceNumber4 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)').text
            EnduranceNumber5 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > div > ul > li:nth-child(5) > textformat > font:nth-child(2)')
            if EnduranceNumber5 is not None:
                EnduranceNumber5 = EnduranceNumber5.text
            else:
                EnduranceNumber5 = "0"

            # 숙련
            Expertise = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)').text
            ExpertiseNumber1 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(1) > textformat > font:nth-child(2)').text
            ExpertiseNumber2 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(2) > textformat > font:nth-child(2)').text
            ExpertiseNumber3 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(3) > textformat > font:nth-child(2)').text
            ExpertiseNumber4 = soup.select_one(
                '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > div > ul > li:nth-child(4) > textformat > font:nth-child(2)')
            if ExpertiseNumber4 is not None:
                ExpertiseNumber4 = ExpertiseNumber4.text
            else:
                ExpertiseNumber4 = "0"

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
                'PowerNumer1': PowerNumber1,
                'PowerNumer2': PowerNumber2,
                'LifeNumer1': LifeNumber1,
                'LifeNumer2': LifeNumber2,
                'CriticalNumer1': CriticalNumber1,
                'CriticalNumer2': CriticalNumber2,
                'SpecializationNumer1': SpecializationNumber1,
                'SpecializationNumer2': SpecializationNumber2,
                'SpecializationNumer3': SpecializationNumber3,
                'SpecializationNumer4': SpecializationNumber4,
                'SpecializationNumer5': SpecializationNumber5,
                'DominationNumer1': DominationNumber1,
                'DominationNumer2': DominationNumber2,
                'DominationNumer3': DominationNumber3,
                'SwiftnessNumer1': SwiftnessNumber1,
                'SwiftnessNumer2': SwiftnessNumber2,
                'SwiftnessNumer3': SwiftnessNumber3,
                'SwiftnessNumer4': SwiftnessNumber4,
                'EnduranceNumer1': EnduranceNumber1,
                'EnduranceNumer2': EnduranceNumber2,
                'EnduranceNumer3': EnduranceNumber3,
                'EnduranceNumer4': EnduranceNumber4,
                'EnduranceNumer5': EnduranceNumber5,
                'ExpertiseNumer1': ExpertiseNumber1,
                'ExpertiseNumer2': ExpertiseNumber2,
                'ExpertiseNumer3': ExpertiseNumber3,
                'ExpertiseNumer4': ExpertiseNumber4
            }
            db.AbilityStatsTooltip.update_one({"name": name}, {'$set': doc}, upsert=True)

            doc = {
                'Engrave': Engrave
            }
            db.Engrave.update_one({"name": name}, {'$set': doc}, upsert=True)

            specialEquipRoute = [
                '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.special-info > div > ul > li:nth-child(1) > div > div > img',
                '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.special-info > div > ul > li:nth-child(2) > div > div > img',
                '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.special-info > div > ul > li:nth-child(3) > div > div > img'
            ]

            specialEquip = []
            for i in specialEquipRoute:

                if soup.select_one(i) is not None:
                    specialEquip.append(soup.select_one(i)['src'])
                else:
                    specialEquip.append("none")

            doc = {'0': specialEquip[0], '1': specialEquip[1], '2': specialEquip[2]}

            db.specialEquip.update_one({"name": name}, {'$set': doc}, upsert=True)
    ###
            browser.find_element(By.XPATH, '//*[@id="profile-ability"]/div[1]/div[1]/a[1]').click()

            tendency0 = browser.find_element(By.XPATH, '//*[@id="chart-states-wrap"]/div[2]/span[1]/span/em').text
            tendency1 = browser.find_element(By.XPATH, '//*[@id="chart-states-wrap"]/div[2]/span[2]/span/em').text
            tendency2 = browser.find_element(By.XPATH, '//*[@id="chart-states-wrap"]/div[2]/span[3]/span/em').text
            tendency3 = browser.find_element(By.XPATH, '//*[@id="chart-states-wrap"]/div[2]/span[4]/span/em').text

            doc = {'0': tendency0, '1': tendency1, '2': tendency2, '3': tendency3}

            db.tendency.update_one({"name": name}, {'$set': doc}, upsert=True)

            ###종열###
            characterImg = soup.select_one('#profile-equipment > div.profile-equipment__character > img')['src']

            equipSlot00 = [soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot1 > img'),
                         soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot2 > img'),
                         soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot3 > img'),
                         soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot4 > img'),
                         soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot5 > img'),
                         soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot6 > img')]

            engraveSlot00 = [soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot14 > img'),
                           soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot15 > img')]

            accessorySlot00 = [soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot7 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot8 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot9 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot10 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot11 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot12 > img'),
                               soup.select_one('#profile-equipment > div.profile-equipment__slot > div.slot13 > img')]

            equipSlot01 = []
            engraveSlot01 = []
            accessorySlot01 = []

            for a in equipSlot00:
                if a is not None:
                    equipSlot01.append(a['src'])
            for a in engraveSlot00:
                if a is not None:
                    engraveSlot01.append(a['src'])
            for a in accessorySlot00:
                if a is not None:
                    accessorySlot01.append(a['src'])

            doc = {'characterImg': characterImg, 'equipSlot': equipSlot01, 'engraveSlot': engraveSlot01, 'accessorySlot': accessorySlot01}

            db.Equips.update_one({"name": name}, {'$set': doc}, upsert=True)

            ###상륜###
            server = soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server').text

            jobImg = soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')['src']

            townLv = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)').text
            fightLv = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').text
            itemLv = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').text
            maxItemLv = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__item > span:nth-child(2)').text

            badge = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__title > span:nth-child(2)').text
            guild = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__guild > span:nth-child(2)').text
            pvp = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.level-info__pvp > span:nth-child(2)').text

            doc = {'server': server, 'jobImg': jobImg, 'townLv': townLv,
                   'fightLv': fightLv, 'itemLv': itemLv, 'maxItemLv': maxItemLv, 'itemLv': itemLv,
                   'badge': badge, 'guild': guild, 'pvp': pvp}

            db.characterInfo.update_one({"name": name}, {'$set': doc}, upsert=True)

            browser.quit()
            return jsonify({'msg': 'suc'})

        except :
            return jsonify({'msg': 'error'})

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

@app.route("/specialEquip", methods=['GET'])
def specialEquip():
    specialEquipImg = db.specialEquip.find_one({'name': f'{name}'}, {'_id': False})

    return jsonify({'specialEquipImg': specialEquipImg})

@app.route("/ability", methods=['GET'])
def ability():
    abilityStats = db.AbilityStats.find_one({'name': f'{name}'}, {'_id': False})
    abilityStatTooltips = db.AbilityStatsTooltip.find_one({'name': f'{name}'}, {'_id': False})
    engrave = db.Engrave.find_one({'name': f'{name}'}, {'_id': False})
    engraveList = engrave['Engrave']

    return jsonify({'abilityStats': abilityStats, 'abilityStatTooltips': abilityStatTooltips, 'engraveList': engraveList})

@app.route("/tendency", methods=['GET'])
def tendency():
    tendency = db.tendency.find_one({'name': f'{name}'}, {'_id': False})

    return jsonify({'tendency': tendency})

#종열 장비 -------------------------------------------------------------------------------------------------------------------------------------

@app.route("/equips", methods=['GET'])
def equips():
    equips = db.Equips.find_one({'name': f'{name}'}, {'_id': False})
    characterImg = equips['characterImg']
    equipSlot = equips['equipSlot']
    accessorySlot = equips['accessorySlot']
    engraveSlot = equips['engraveSlot']

    return jsonify({'characterImg': characterImg, 'equipSlot': equipSlot, 'accessorySlot': accessorySlot, 'engraveSlot': engraveSlot})

# 상륜 정보 -------------------------------------------------------------------------------------------------------------------------------------

@app.route("/characterInfo", methods=['GET'])
def info():
    characterInfo = db.characterInfo.find_one({'name': f'{name}'}, {'_id': False})
    characterName = name
    return jsonify({'characterInfo': characterInfo, 'characterName': characterName})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
