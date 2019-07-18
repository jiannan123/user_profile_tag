# author:zhengjiannan
# datetime:2019/4/4 19:44
from utils import getStartUids
from weibo import WeiboUidTool
from time import sleep

start_uids = getStartUids("startweibo.conf")
num = 0
for uid in start_uids:
    wbt = WeiboUidTool(uid)     #初始化对象
    print(wbt.get_fans_uid_by_fans_list(uid))    #获取用户对应的粉丝uid
    print(wbt.get_follows_uid_by_follow_list(uid))      #获取用户对应的关注uid
    print(uid)
    num += wbt.fans_num
    num += wbt.follow_num
    sleep(15)
print("\n" + str(num))

