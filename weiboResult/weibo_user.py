# -*- coding: utf-8 -*-

from flask import Flask,jsonify,render_template,send_from_directory,Response,session,request
from pymongo import MongoClient
from wordcloud import WordCloud
from datetime import timedelta
import json
import os

app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
#session.permanent = True
app.permanent_session_lifetime = timedelta(seconds=1)
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = "123"
conn = MongoClient('127.0.0.1', 27017)
db = conn.weibo_info  # 访问weibo_info数据库
user = db.user_tag  # 选择表user_tag
iscomplete = 0

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getTag')
def getTag():
    context = {
        'results': user.find().sort([("_id", 1)])
    }
    img_src = "../static/images/pre.jpg"
    return render_template('user.html', **context, img_src=img_src)


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        print(data)
        name = data['name']
        label = data['label']
        _tag = data['_tag']
        tag = _tag.split()
        text = data['text']
        for i in user.find({"name": name}):
            if i['text'] == text and i['label'] == label and i['tag'] == tag:
                data['result'] = 2
            else:
                user.update({"name": name}, {'$set': {"label": label}})
                user.update({"name": name}, {'$set': {"text": text}})
                user.update({"name": name}, {'$set': {"_tag": _tag}})
                user.update({"name": name}, {'$set': {"tag": tag}})
                data['result'] = 1
                iscomplete == 0
        return jsonify(data)


@app.route("/download", methods=['GET'])
def downloader():
    #连接数据库

    #获取词汇集
    tag = []
    result = ""
    for it in user.find():
        if it["name"] not in tag:
            tag.append(it["name"])
            result += it["name"] + " "
        if it["label"] not in tag:
            tag.append(it["label"])
            result += it["label"] + " "
        for word in it["tag"]:
            if word not in tag:
                tag.append(word)
                result += word + " "

    ans = result.split()
    ans.reverse()
    res = ""
    for word in ans:
        res += word + " "

    #生成词云图
    if iscomplete == 0:
        cloud = WordCloud(font_path="C:/Windows/Fonts/msyhl.ttc", background_color="white", width=600, height=400,
                      max_words=150).generate(res)
        image = cloud.to_image()
        #image.show()
        image.save("D:\py_practice\weiboResult\static\images\wordcloud.jpg")
        iscomplete == 1
    #将图片结果返回
    context = {
        'results': user.find().sort([("_id", 1)])
    }
    img_src = "../static/images/wordcloud.jpg"
    return render_template('user.html', **context, img_src=img_src)

if __name__ == "__main__":
    app.run(debug=True)
    conn.close()
