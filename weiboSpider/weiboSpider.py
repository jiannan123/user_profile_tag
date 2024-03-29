#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import requests
import sys
import traceback
import pymysql
from datetime import datetime
from datetime import timedelta
from lxml import etree
from tqdm import tqdm
from time import sleep

conn = pymysql.connect(host='localhost', user='root', passwd='uisf1002', charset='utf8', port=3306)
cur = conn.cursor()
conn.select_db("weibo_info")

class Weibo:
    cookie = {"Cookie": "_T_WM=3274a31eff8d2c3000840164d47657a3; ALF=1557210185; SCF=Ap6PHCbbtAjEl0Rxhcq1LGH_AznL9QMa-Q2w8Xm"
                  "1rfnbl-iH25t5LS8SuKBdhoErIvwD2vma6jBTcvCpoxVlbIw.; SUB=_2A25xrdjmDeRhGeNJ6VYT8yjJyz6IHXVTUfiurDV6PU"
                  "JbktANLU7HkW1NS_DSaDc3VPUmHZfXq9kJ6I3u5pXPCpXc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56GZlNXYup01"
                  "z8Xn7mXKDO5JpX5K-hUgL.Fo-NeoBEe0qfehz2dJLoI0qLxKBLB.BLBK5LxKML1-2L1hBLxKnL12zL12qLxKqL1h.L1KeLxK."
                  "LBK-LB.eLxK-LBo.LBozt; SUHB=0Jvgym9L8bKQ48"}
    # Weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.weibo_place = []  # 微博位置
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数
        self.publish_tool = []  # 微博发布工具

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print(u"用户名: " + self.username)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            #微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print(u"微博数: " + str(self.weibo_num))

            #关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print(u"关注数: " + str(self.following))

            #粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print(u"粉丝数: " + str(self.followers))
            print(
                "===========================================================================")

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取"长微博"全部文字内容
    def get_long_weibo(self, weibo_link):
        try:
            html = requests.get(weibo_link, cookies=self.cookie).content
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = info.xpath("div/span[@class='ctt']")[0].xpath(
                "string(.)").replace(u"\u200b", "").encode(sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取转发微博信息
    def get_retweet(self, is_retweet, info, wb_content):
        try:
            original_user = is_retweet[0].xpath("a/text()")
            if not original_user:
                wb_content = u"转发微博已被删除"
                return wb_content
            else:
                original_user = original_user[0]
            retweet_reason = info.xpath("div")[-1].xpath("string(.)").replace(u"\u200b", "").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            retweet_reason = retweet_reason[:retweet_reason.rindex(u"赞")]
            wb_content = (retweet_reason + "\n" + u"原始用户: " +
                          original_user + "\n" + u"转发内容: " + wb_content)
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博内容
    def get_weibo_content(self, info):
        try:
            str_t = info.xpath("div/span[@class='ctt']")
            weibo_content = str_t[0].xpath("string(.)").replace(u"\u200b", "").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            weibo_id = info.xpath("@id")[0][2:]
            a_link = info.xpath("div/span[@class='ctt']/a")
            is_retweet = info.xpath("div/span[@class='cmt']")
            if a_link:
                if a_link[-1].xpath("text()")[0] == u"全文":
                    weibo_link = "https://weibo.cn/comment/" + weibo_id
                    wb_content = self.get_long_weibo(weibo_link)
                    if wb_content:
                        if not is_retweet:
                            wb_content = wb_content[1:]
                        weibo_content = wb_content
            if is_retweet:
                weibo_content = self.get_retweet(
                    is_retweet, info, weibo_content)
            self.weibo_content.append(weibo_content)
            print(weibo_content)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # # 获取微博发布位置
    # def get_weibo_place(self, info):
    #     try:
    #         div_first = info.xpath("div")[0]
    #         a_list = div_first.xpath("a")
    #         weibo_place = u"无"
    #         for a in a_list:
    #             if ("place.weibo.com" in a.xpath("@href")[0] and
    #                     a.xpath("text()")[0] == u"显示地图"):
    #                 weibo_a = div_first.xpath("span[@class='ctt']/a")
    #                 if len(weibo_a) >= 1:
    #                     weibo_place = weibo_a[-1]
    #                     if u"的秒拍视频" in div_first.xpath("span[@class='ctt']/a/text()")[-1]:
    #                         if len(weibo_a) >= 2:
    #                             weibo_place = weibo_a[-2]
    #                         else:
    #                             weibo_place = u"无"
    #                     weibo_place = weibo_place.xpath("string(.)").encode(
    #                         sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
    #                     break
    #         self.weibo_place.append(weibo_place)
    #         print(u"微博位置: " + weibo_place)
    #     except Exception as e:
    #         print("Error: ", e)
    #         traceback.print_exc()

    # 获取微博发布时间
    def get_publish_time(self, info):
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = str_time[0].xpath("string(.)").encode(
                sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
            publish_time = str_time.split(u'来自')[0]
            if u"刚刚" in publish_time:
                publish_time = datetime.now().strftime(
                    '%Y-%m-%d %H:%M')
            elif u"分钟" in publish_time:
                minute = publish_time[:publish_time.find(u"分钟")]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() - minute).strftime(
                    "%Y-%m-%d %H:%M")
            elif u"今天" in publish_time:
                today = datetime.now().strftime("%Y-%m-%d")
                time = publish_time[3:]
                publish_time = today + " " + time
            elif u"月" in publish_time:
                year = datetime.now().strftime("%Y")
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = (year + "-" + month + "-" + day + " " + time)
            else:
                publish_time = publish_time[:16]
            self.publish_time.append(publish_time)
            print(u"微博发布时间: " + publish_time)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博发布工具
    # def get_publish_tool(self, info):
    #     try:
    #         str_time = info.xpath("div/span[@class='ct']")
    #         str_time = str_time[0].xpath("string(.)").encode(
    #             sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
    #         if len(str_time.split(u'来自')) > 1:
    #             publish_tool = str_time.split(u'来自')[1]
    #         else:
    #             publish_tool = u"无"
    #         self.publish_tool.append(publish_tool)
    #         print(u"微博发布工具: " + publish_tool)
    #     except Exception as e:
    #         print("Error: ", e)
    #         traceback.print_exc()

    # 获取用户微博信息
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            if page_num > 2:
                page_num = 2
            pattern = r"\d+\.?\d*"
            for page in tqdm(range(1, page_num + 1), desc=u"进度"):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                is_empty = info[0].xpath("div/span[@class='ctt']")
                if is_empty:
                    for i in range(0, len(info) - 2):

                        # 微博内容
                        self.get_weibo_content(info[i])

                        # # 微博位置
                        # self.get_weibo_place(info[i])
                        #
                        # 微博发布时间
                        self.get_publish_time(info[i])
                        #
                        # # 微博发布工具
                        # self.get_publish_tool(info[i])

                        str_footer = info[i].xpath("div")[-1]
                        str_footer = str_footer.xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        str_footer = str_footer[str_footer.rfind(u'赞'):]
                        guid = re.findall(pattern, str_footer, re.M)

                        # 点赞数
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        print(u"点赞数: " + str(up_num))

                        # 转发数
                        retweet_num = int(guid[1])
                        self.retweet_num.append(retweet_num)
                        print(u"转发数: " + str(retweet_num))

                        # 评论数
                        comment_num = int(guid[2])
                        self.comment_num.append(comment_num)
                        print(u"评论数: " + str(comment_num))
                        print(
                            "===========================================================================")

                        self.weibo_num2 += 1

            if not self.filter:
                print(u"共" + str(self.weibo_num2) + u"条微博")
            else:
                print(u"共" + str(self.weibo_num) + u"条微博，其中" +
                      str(self.weibo_num2) + u"条为原创微博"
                      )
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 将爬取的信息写入文件
    def write_txt(self):
        try:
            if self.weibo_num2 >= 5:
                insert_user_info(self.user_id,self.username,self.followers,self.following)
                for i in range(1, self.weibo_num2 + 1):
                    tmp = str(self.weibo_content[i - 1])
                    print(self.publish_time[i - 1])
                    insert_user_text(self.user_id,self.weibo_content[i - 1],self.publish_time[i - 1],self.retweet_num[i - 1],self.comment_num[i - 1])
                conn.commit()
            #     if self.weibo_num2 >= 5:
            #     #     result = (str(self.user_id) +
            #     #           u"\r\n" + self.username +
            #     #           u"\r\n" + str(self.weibo_num) +
            #     #           u"\r\n" + str(self.following) +
            #     #           u"\r\n" + str(self.followers) +
            #     #           u"\r\n")
            #         result = ""
            #         for i in range(1, self.weibo_num2 + 1):
            #             text = (str(i) + ":" + self.weibo_content[i - 1] + "\r\n"
            #                 # u"微博位置: " + self.weibo_place[i - 1] + "\n" +
            #                 #u"发布时间: " + self.publish_time[i - 1] + "\r\n\n"
            #                 # u"点赞数: " + str(self.up_num[i - 1]) +
            #                 # u"   转发数: " + str(self.retweet_num[i - 1]) +
            #                 # u"   评论数: " + str(self.comment_num[i - 1]) + "\n\n,"
            #                 # u"发布工具: " + self.publish_tool[i - 1] + "\n\n"
            #                 )
            #             result += text
            #         file_dir = os.path.split(os.path.realpath(__file__))[
            #             0] + os.sep + "weibo_414"
            #         if not os.path.isdir(file_dir):
            #             os.mkdir(file_dir)
            #         file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            #         f = open(file_path, "wb")
            #         f.write(result.encode(sys.stdout.encoding))
            #         f.close()
            #         print(u"微博写入文件完毕，保存路径:")
            #         print(file_path)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.write_txt()
            print(u"信息抓取完毕")
            print(
                "===========================================================================")
        except Exception as e:
            print("Error: ", e)

def insert_user_info(uid,uname,ufans,ufollows):
    insert_value = (uid,uname,ufans,ufollows)
    cur.execute('insert into user_info(uid,user_name,user_fans,user_follows) values(%s,%s,%s,%s)', insert_value)
    conn.commit()
def insert_user_text(uid,utext,rtime,fnum,cnum):
    insert_value = (uid,utext,rtime,fnum,cnum)
    cur.execute('insert into user_weibo_text(uid,user_text,release_time,'
                'forwarding_number,comment_number) values(%s,%s,%s,%s,%s)', insert_value)
    #conn.commit()
def main():
    try:
        # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
        file_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + "conf" + os.sep + "1.txt"
        exist = []
        for word in open(file_path,"r"):
            if word not in exist:
                exist.append(word)
                user_id = int(word)  # 可以改成任意合法的用户id（爬虫的微博id除外）
                filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
                wb = Weibo(user_id, filter)  # 调用Weibo类，创建微博实例wb
                wb.start()  # 爬取微博信息
                print(u"用户id: " + word)
                print(u"用户名: " + wb.username)
                print(u"全部微博数: " + str(wb.weibo_num))
                print(u"关注数: " + str(wb.following))
                print(u"粉丝数: " + str(wb.followers))
                sleep(5)
                # if wb.weibo_content:
                #     print(u"最新/置顶 微博为: " + wb.weibo_content[0])
                #     #print(u"最新/置顶 微博位置: " + wb.weibo_place[0])
                #     print(u"最新/置顶 微博发布时间: " + wb.publish_time[0])
                #     print(u"最新/置顶 微博获得赞数: " + str(wb.up_num[0]))
                #     print(u"最新/置顶 微博获得转发数: " + str(wb.retweet_num[0]))
                #     print(u"最新/置顶 微博获得评论数: " + str(wb.comment_num[0]))
                #     #print(u"最新/置顶 微博发布工具: " + wb.publish_tool[0])
    except Exception as e:
        print("Error: ", e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
    cur.close()
    conn.close()
    # text = "1:人生是由许多不完美连缀成的完美曲线，不要为曾经的错" \
    #        "失忿忿不平，无须为走远的风景扼腕叹息。我们要知道，完美的是想象，不完美的才是生活。过去就如一张封口照片，只可以借鉴和欣赏，却无法颠倒和重复。昨天是定型的一本书，今天是待绘的一张纸，我们不能让太多的过往挤压当下的空间！ #满满都是正能量[超话]#"
    # insert_user_info("12345","123",123,256)
    # insert_user_text("12345",text,"111",123,555)
    # conn.commit()
