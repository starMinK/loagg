# import re
import requests
from bs4 import BeautifulSoup
# import json
#
# lv3_url = 'https://lostark.game.onstove.com/Profile/Character/123'
# page_source = requests.get(lv3_url).text
# matched00 = re.search('Profile = {(.+?)};', page_source, re.S)
# matched01 = re.search('"Equip":(.+?)"E459416e_000"', page_source, re.S)
# json_string = matched00.group(1).strip()
#
# course_list = json.loads(json_string)
#
# print(json_string)
#
# # for course in course_list:
# #     print('{name} {url}'.format(**course))
# #
# # print(page_source)


# post저장
# delete없애기
# put업데이트
# get가져오기
#
# 저장:
# type:post
# url:'/api/save-info'
# data:

# ability어빌리티
# power공격력 수치
# life최대 생명력 수치
#
# stats스텟
# critical치명 수치
# specialization특화 수치
# suppress제압 수치
# fast신속 수치
# patience인내 수치
# skill숙련 수치
#
# 각인
# 각인효과 안에들어가는 텍스트
#
# 성향
# 지성 수치
# 담력 수치
# 매력 수치
# 친절 수치
#
# 스페셜
# 특수장비 이미지 +텍스트
client = MongoClient('mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.loagg

app = Flask(__name__)


@app.route("/api/save-info", methods=["POST"])
def save_ability():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/123', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    abilityDoc = {
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(2)')
    }

    statsDoc = {
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)'),
        soup.select_one('#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(1)')
    }

    doc = {abilityDoc, statsDoc}
    db.ability.insert_one(doc)
