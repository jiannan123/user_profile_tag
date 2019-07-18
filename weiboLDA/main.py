import os
import sys
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import lda.datasets
from pymongo import MongoClient

if __name__ == "__main__":
    lines = []
    # conn = MongoClient('127.0.0.1', 27017)
    # db = conn.weibo_info
    # user = db.user_tag
    file_dir = "D:\\py_practice\\weiboSpider\\weibo_user"
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path = file_dir + os.sep + file
            line = open(file_path, "r", encoding="utf-8").read()
            lines.append(line.strip())
    vectorizer = CountVectorizer()
    # print(vectorizer)
    X = vectorizer.fit_transform(lines)  # fit_transform函数将文本中的词语转换为词频矩阵
    # print(vectorizer.get_feature_names())
    analyse = vectorizer.build_analyzer()
    # X_scaler = StandardScaler()
    # X = X_scaler.fit_transform(X)
    # pca = PCA(n_components=0.85)  # 保证降维后的数据保持90%的信息
    # pca.fit(X)
    # weight = X.toarray()
    # print(weight)
    word = vectorizer.get_feature_names()
    print(word)

    model = lda.LDA(n_topics=25, n_iter=500, random_state=1)
    model.fit_transform(X)
    topic_word = model.topic_word_

    # 输出主题中的TopN关键词
    print(topic_word[:, :10])

    n = 15
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(word)[np.argsort(topic_dist)][:-(n + 1):-1]
        print(u'*Topic {}\n {}'.format(i, ' '.join(topic_words)))
    #     result = ""
    #     for it in topic_words:
    #         result += it + " "
    #     user.insert({"name": "Topic" + str(i), "text": result})
    #
    # conn.close()


    # 文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

    # 输出前10篇文章最可能的Topic
    label = []
    for n in range(10):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
        print("doc: {} topic: {}".format(n, topic_most_pr))

