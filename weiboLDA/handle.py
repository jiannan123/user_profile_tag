import os
import sys

#初始阶段将所有的文本内容整合到一个文件里，现在已经用处不大了
if __name__ == "__main__":
    file_dir = "D:\\py_practice\\weiboSpider\\weibo_user"
    file_path3 = file_dir + os.sep + "all.txt"
    f = open(file_path3, "ab")
    print(file_path3)
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path = file_dir + os.sep + file
            article = open(file_path, "r", encoding="utf-8").read()
            article += " "
            f.write(article.encode(sys.stdout.encoding))
    f.close()
