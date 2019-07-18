# -*- coding: utf-8 -*-


from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.weibo_info  # 访问weibo_info数据库
user = db.user_tag  # 选择表user_tag

#更新数据库文档的一些数据域
for result in user.find():
    str1 = " ".join(str(i) for i in result['tag'])
    print(str1)
    name = result['_id']
    user.update({"_id": name}, {'$set': {"_tag": str1}})

