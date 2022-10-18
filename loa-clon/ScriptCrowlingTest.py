import re
import requests
import json

lv3_url = 'https://lostark.game.onstove.com/Profile/Character/123'
page_source = requests.get(lv3_url).text
matched00 = re.search('Profile = {(.+?)};', page_source, re.S)
matched01 = re.search('"Equip":(.+?)"E459416e_000"', page_source, re.S)
json_string = matched00.group(1).strip()

course_list = json.loads(json_string)

print(json_string)

# for course in course_list:
#     print('{name} {url}'.format(**course))
#
# print(page_source)