import os
import traceback


def main():  #处理初始文本数据时，跳过前5行的非文本内容
    file_dir = os.path.split(os.path.realpath(__file__))[0]
    print(file_dir)
    file_path1 = file_dir + os.sep + "weibo"
    for root, dirs, files in os.walk(file_path1):
        for file in files:
            try:
                file_path2 = file_dir + os.sep + "weibo" + os.sep + file
                file_path3 = file_dir + os.sep + "weibo_tmp" + os.sep + file
                f = open(file_path3, "wb")
                lines = open(file_path2,"rb").readlines()
                if lines:
                    for line in lines[5:]:
                        f.write(line)
                f.close()
            except Exception as e:
                print("Error: ", e)
                traceback.print_exc()



if __name__ == "__main__":
    main()
