import os
import traceback
import pymysql


conn = pymysql.connect(host='localhost', user='root', passwd='uisf1002', charset='utf8', port=3306)
cur = conn.cursor()
conn.select_db("weibo_info")


def main():
    file_dir = os.path.split(os.path.realpath(__file__))[0]
    file_path1 = file_dir + os.sep + "weibo_user"
    for root, dirs, files in os.walk(file_path1):
        for file in files:
            try:
                uid = file.split('.', -1)
                file_path1 = file_dir + os.sep + "weibo_user" + os.sep + file
                article = open(file_path1, "r", encoding="utf-8").read()
                insert_value = (uid[0], article)
                print(uid[0])
                cur.execute('insert into user_text_handled(uid,user_text_handled) values(%s,%s)',insert_value)
                conn.commit()
            except Exception as e:
                print("Error: ", e)
                traceback.print_exc()


if __name__ == "__main__":
    main()
