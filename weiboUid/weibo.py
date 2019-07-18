import requests
from lxml import etree
from urllib import request
import selectors
from bs4 import BeautifulSoup
import re
import sys
import traceback
import os
from utils import isWeiboHomeUrlPattern
from settings import cookie


class WeiboUidTool:

    def __init__(self, uid):
        self.fans_num = 0
        self.follow_num = 0
        self.uid = uid

    def get_friend_url_by_follow_or_fan_list(self, url):
        """
        通过微博的关注列表或者分析列表获取关注人或者粉丝的home url
        :param url: 用户的关注或粉丝页的url
        如：
        关注页：https://weibo.cn/1799599962/follow?page=1
        粉丝页：https://weibo.cn/1799599962/fans?page=1
        :return: 一个包含多个url的list
        """
        home_urls = []
        html = requests.get(url, cookies=cookie).content
        soup = BeautifulSoup(html, features="html.parser")
        tables = soup.select("table")
        if len(tables) > 0:
            re_pattern = r'<td valign="top"><a href="(.*?)">'
            for table in tables:
                url = re.search(re_pattern, str(table)).group(1)
                # print(url)
                home_urls.append(url)
        return home_urls

    def get_uid_by_home_url(self, url):
        html = requests.get(url, cookies=cookie).content
        # soup = BeautifulSoup(html, features="html.parser")
        re_pattern = r'关注.*<a href="/(.*?)/fans">粉丝'
        uid = re.search(re_pattern, html.decode())
        if uid:
            uid = uid.group(1)
        else:
            uid = ""
        return uid

    def write_txt(self, uids):
        try:
            result = ""
            for id in uids:
                result += str(id) + "\r\n"
            print(result)
            file_dir = "D:\\py_practice\\weiboSpider\\conf\\weibo_uid_414.txt"
            f = open(file_dir, "ab")
            f.write(result.encode(sys.stdout.encoding))
            f.close()
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_fans_uid_by_fans_list(self, uid):
        home_urls = []
        uids = []
        for page in range(1, 21):
            url = "https://weibo.cn/{}/fans?page={}".format(uid, page)
            page_urls = self.get_friend_url_by_follow_or_fan_list(url)
            if len(page_urls) == 0:
                break
            home_urls += page_urls
        num = 0
        for url in home_urls:
            if isWeiboHomeUrlPattern(url):
                uid = url[19:]
            else:
                uid = self.get_uid_by_home_url(url)
            num += 1
            if num > 50:
                break
            uids.append(uid)
            self.fans_num += 1
        self.write_txt(uids)
        return uids

    def get_follows_uid_by_follow_list(self, uid):
        home_urls = []
        uids = []
        for page in range(1, 21):
            url = "https://weibo.cn/{}/follow?page={}".format(uid, page)
            page_urls = self.get_friend_url_by_follow_or_fan_list(url)
            if len(page_urls) == 0:
                break
            home_urls += page_urls
        num = 0
        for url in home_urls:
            if isWeiboHomeUrlPattern(url):
                uid = url[19:]
            else:
                uid = self.get_uid_by_home_url(url)
            num += 1
            if num > 150:
                break
            uids.append(uid)
            self.follow_num += 1
        self.write_txt(uids)
        return uids












