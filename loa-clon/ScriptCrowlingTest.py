import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/123', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

abilityEngrave = soup.select_one('#chart-states-wrap > div.states_box')
# text = abilityEngrave.split('\n\n\n')
print(abilityEngrave)
# split, index
# print(text)
