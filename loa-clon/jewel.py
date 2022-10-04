from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

client = MongoClient('mongodb+srv://idvalue:passwordvalue@Cluster0.vlj5yqv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)