from flask import Flask, render_template, request, jsonify, app
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
#규민db
#mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority
#내db
#mongodb+srv://test:sparta@cluster0.s7gsuon.mongodb.net/Cluster0?retryWrites=true&w=majority
client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.s7gsuon.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.loagg

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://lostark.game.onstove.com/Profile/Character/%EC%84%B1%EC%88%98%EB%8F%99%EA%BF%80%EA%BD%88%EB%B0%B0%EA%B8%B0',
                    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
name = '수테비아'
cardlist = [soup.select_one('#cardList > li:nth-child(1)'),
            soup.select_one('#cardList > li:nth-child(2)'),
            soup.select_one('#cardList > li:nth-child(3)'),
            soup.select_one('#cardList > li:nth-child(4)'),
            soup.select_one('#cardList > li:nth-child(5)'),
            soup.select_one('#cardList > li:nth-child(6)'),
            ]
cardimglist = []
cardnamelist = []
cardawakelist = []

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
    }
    db.cardlist.update_one({"name": name}, {'$set': doc}, upsert=True)

print(cardnamelist)
print(cardimglist)
print(cardawakelist)


