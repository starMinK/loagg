from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://LOAGG:spatrateam4LOAGGprojectpassword@Cluster1.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.loagg

app = Flask(__name__)

name = ""

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/main')
def main():
    return render_template('main.html')

#search에서 name 받아오기
@app.route("/api/names", methods=["POST"])
def save_name():
    name = request.form['name_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(f'https://lostark.game.onstove.com/Profile/Character/{name}', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    slot00 = soup.select_one("#gem00 > span.jewel_img > img")['src']
    slot01 = soup.select_one("#gem01 > span.jewel_img > img")['src']
    slot02 = soup.select_one("#gem02 > span.jewel_img > img")['src']
    slot03 = soup.select_one("#gem03 > span.jewel_img > img")['src']
    slot04 = soup.select_one("#gem04 > span.jewel_img > img")['src']
    slot05 = soup.select_one("#gem05 > span.jewel_img > img")['src']
    slot06 = soup.select_one("#gem06 > span.jewel_img > img")['src']
    slot07 = soup.select_one("#gem07 > span.jewel_img > img")['src']
    slot08 = soup.select_one("#gem08 > span.jewel_img > img")['src']
    slot09 = soup.select_one("#gem09 > span.jewel_img > img")['src']
    slot10 = soup.select_one("#gem10 > span.jewel_img > img")['src']

    doc = {
        'name': name,
        'gem00': slot00,
        'gem01': slot01,
        'gem02': slot02,
        'gem03': slot03,
        'gem04': slot04,
        'gem05': slot05,
        'gem06': slot06,
        'gem07': slot07,
        'gem08': slot08,
        'gem09': slot09,
        'gem10': slot10,
    }

    print(slot00)

    return ""

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)