from pymongo import MongoClient

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.weibo_info   #访问weibo_info数据库
    user = db.user_tag   #选择表user_tag
    for it in user.find():
        _id = it["_id"]
        print(it["text"])
        print("该主题的初始标签：" + it["name"])
        print("该主题的初始主标签：" + it["label"])
        print("该主题的初始子标签：")
        for i in it["tag"]:
            print(i + " ")
        tag = []
        user_tag = input("请输入该主题对应的标签：")
        if len(user_tag) == 0:
            user_tag = it["name"]
        label = input("请输入该主题对应的主标签：")
        if len(label) == 0:
            label = it["label"]
        tmp = input("请输入该主题标签包含的子标签：")
        tag = tmp.split()
        if len(tag) == 0:
            tag = it["tag"]
        user.update({"_id": _id}, {'$set': {"name": user_tag}})
        user.update({"_id": _id}, {'$set': {"label": label}})
        user.update({"_id": _id}, {'$set': {"tag": tag}})

    conn.close()
