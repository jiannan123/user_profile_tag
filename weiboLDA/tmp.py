import os
import sys
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import StandardScaler
import lda.datasets
import time

def print_top_words(model, feature_names, n_top_words):
    #打印每个主题下权重较高的term
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    #打印主题-词语分布矩阵
    print(model.components_)


if __name__ == "__main__":
    lines = []
    model_path = "D:\\py_practice\\weiboLDA\\model\\model.m"
    file_dir = "D:\\py_practice\\weiboSpider\\weibo_user"
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path = file_dir + os.sep + file
            line = open(file_path, "r", encoding="utf-8").read()
            lines.append(line.strip())

    vectorizer = CountVectorizer(max_df=0.9,min_df=2)
    X = vectorizer.fit_transform(lines)   #fit_transform函数将文本中的词语转换为词频矩阵
    joblib.dump(X, model_path)

    # n_topic = 30
    # lda = LatentDirichletAllocation(n_components=n_topic,
    #                                     max_iter=500,
    #                                     learning_method='batch')
    # lda.fit(X)
    # feature_name = vectorizer.get_feature_names()
    # print_top_words(lda,feature_name,20)


    n_topics = range(10, 100, 5)
    perplexityLst = [1.0] * len(n_topics)

    # 训练LDA并打印训练时间
    lda_models = []
    for idx, n_topic in enumerate(n_topics):
        lda = LatentDirichletAllocation(n_components=n_topic,
                                        max_iter=200,
                                        learning_method='batch')
        #t0 = time()
        lda.fit(X)
        perplexityLst[idx] = lda.perplexity(X)
        lda_models.append(lda)
        print("Topics: %d\n " % n_topics[idx])
        print("Perplexity Score %0.3f\n" % perplexityLst[idx])

    # 打印最佳模型
    best_index = perplexityLst.index(min(perplexityLst))
    best_n_topic = n_topics[best_index]
    best_model = lda_models[best_index]
    print("Best Topic: " + str(best_n_topic))

    # 绘制不同主题数perplexity的不同
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(n_topics, perplexityLst)
    ax.set_xlabel("Topics")
    ax.set_ylabel("Approximate Perplexity")
    plt.grid(True)
    #plt.savefig(os.path.join('lda_result', 'perplexityTrend' + CODE + '.png'))
    plt.show()









