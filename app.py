import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient

from datetime import datetime

MONGODB_URI = os.environ.get("MONGO_DB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-T%H-%M-%S')
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    pp = request.files['profile_give']
    pp_extension = pp.filename.split('.')[-1]
    pp_filename = f'static/profile/pp-{mytime}.{pp_extension}'
    pp.save(pp_filename)
    
    timestamps = today.strftime('%Y.%m.%d | %H:%M:%S')

    
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")
    doc = {
        'pp': pp_filename,
        'file': filename,
        'title':title_receive,
        'content':content_receive,
        'time': timestamps
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)