import os
import jieba
import traceback
import sys
import re

def Jieba(uid, stopwords):
    file_dir = os.path.split(os.path.realpath(__file__))[0]
    # 用来保存需要读取的文件路径
    file_path = file_dir + os.sep + "weibo" + os.sep + uid
    article = open(file_path, "r", encoding="utf-8").read()
    words = jieba.cut(article, cut_all=False)
    result = ""
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    for word in words:
        if word not in stopwords:
            match = zhPattern.search(word)
            if match and len(word) > 1:
                result += word + " "
    print("result:\n" + result)
    file_path3 = file_dir + os.sep + "weibo_user" + os.sep + uid
    f = open(file_path3, "wb")
    f.write(result.encode(sys.stdout.encoding))
    f.close()
    print(file_path3)

def main():
    # 用来保存需要去除的停用词
    stopwords = []
    file_dir = os.path.split(os.path.realpath(__file__))[0]
    # 加载自定义词库，防止出现无法识别的词语
    jieba.load_userdict(file_dir + os.sep + "conf" + os.sep + "user_defined_words.txt")
    #file_path1 = file_dir + os.sep + "conf" + os.sep + "weibo_uid.txt"
    file_path2 = file_dir + os.sep + "conf" + os.sep + "stop_words.txt"
    for word in open(file_path2, "r"):
        stopwords.append(word.strip())
    stopwords.append("\n")
    # print(stopwords)
    for root, dirs, files in os.walk(file_dir + os.sep + "weibo"):
        for file in files:
            try:
                Jieba(file, stopwords)
            except Exception as e:
                print("Error: ", e)
                traceback.print_exc()
    # for word in open(file_path1, "r"):
    #     try:
    #         uid = int(word)
    #         Jieba(str(uid), stopwords)
    #     except Exception as e:
    #         print("Error: ", e)
    #         traceback.print_exc()


if __name__ == "__main__":
    main()
