from flask import Flask, render_template, request, jsonify, app
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.s7gsuon.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://lostark.game.onstove.com/Profile/Character/%EC%88%98%ED%85%8C%EB%B9%84%EC%95%84',
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
    db.loagg.update_one({"name": name,'num': num}, {'$set': doc}, upsert=True)
