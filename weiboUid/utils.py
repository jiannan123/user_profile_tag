import re


def getStartUids(filepath):
    """
            读取配置文件，文件中每行为一个user id
            return list,list中保存有所有开始爬取的user id
    """
    with open(filepath) as f:
        uids = []
        lines = f.readlines()
        for line in lines:
            uids.append(line.strip())
        return uids


def isWeiboHomeUrlPattern(url):
    """
    判断一个url字符串是否满足如下的模式
    https://weibo.cn/u/6934723786
    :param url: 字符串
    :return: true or false
    """
    re_pattern = r'https://weibo.cn/u/(.*)'
    ret = re.search(re_pattern, url)
    if ret:
        return True
    else:
        return False


def loginWeibo(username, password):
    pass

