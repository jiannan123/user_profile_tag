from pymongo import MongoClient
from wordcloud import WordCloud

if __name__ == "__main__":
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.weibo_info  # 访问weibo_info数据库
    user = db.user_tag  # 选择表user_tag
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
    print(res)
    cloud = WordCloud(font_path="C:/Windows/Fonts/msyhl.ttc", background_color="white", width=600, height=300, max_words=100).generate(res)
    image = cloud.to_image()
    image.show()
    image.save("111.jpg")




