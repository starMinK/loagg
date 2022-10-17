from flask import Flask, render_template, request, jsonify, app
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.loagg

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://lostark.game.onstove.com/Profile/Character/%EB%B0%94%EB%93%9C%ED%9D%AC',
                    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
cardlist = soup.select('#cardList > li')
name = '수테비아'
num = 0;
for card in cardlist:
    cardname = card.select_one('div > strong > font').text
    cardimg = card.select_one('div > img')['src']
    cardawake = card.select_one('div')['data-awake']
    print(cardname, cardimg, cardawake)
    num += 1;

    doc = {
        'num': num,
        'name': name,
        'cardname': cardname,
        'cardimg': cardimg,
        'cardawake': cardawake
    }
    db.cardlist.update_one({"name": name,'num': num}, {'$set': doc}, upsert=True)





