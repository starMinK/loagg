import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

#selenium
url = 'https://lostark.game.onstove.com/Profile/Character/123'
browser = webdriver.Chrome()
browser.get(url)

#request
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/123', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
for a in list:
        browser.find_element(By.XPATH, '//*[@id="profile-ability"]/div[1]/div[1]/a[3]').click()

        browser.find_element(By.XPATH, f'//*[@id="gem{a}"]').click()
        effect = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[5]').text

        print(effect)
# //*[@id="gem00"]
# //*[@id="gem01"]
# //*[@id="gem10"]


'''
#보석 이름
testTitle = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[1]/p/font')
# //*[@id="lostark-wrapper"]/div[2]/div[1]/p/font
# //*[@id="lostark-wrapper"]/div[2]/div[1]/p/font
#보석 이미지
testImg = browser.find_element(By.XPATH, '//*[@id="lostark-wrapper"]/div[2]/div[2]/span[1]/img')
#보석 등급
# //*[@id="lostark-wrapper"]/div[2]/div[2]/span[2]/font/font

#보석 티어
# //*[@id="lostark-wrapper"]/div[2]/div[2]/span[4]/font

#보석 거래 유무
# //*[@id="lostark-wrapper"]/div[2]/div[3]/span[2]

#보석 레벨
# //*[@id="lostark-wrapper"]/div[2]/div[4]
# //*[@id="lostark-wrapper"]/div[2]/div[4]

#보석 효과
# //*[@id="lostark-wrapper"]/div[2]/div[5]/text()[1]
# //*[@id="lostark-wrapper"]/div[2]/div[5]/font[2]
# //*[@id="lostark-wrapper"]/div[2]/div[5]/text()[2]

#분해 유무
# //*[@id="lostark-wrapper"]/div[2]/div[6]/font/font



# time.sleep(2)
# test = soup.select_one('//*[@id="lostark-wrapper"]/div[2]/div[2]/span[1]/img')
'''
# print(testImg.get_attribute('src'))
