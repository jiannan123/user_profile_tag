1、conf文件夹中的文件简介
① stop_words.txt
用来保存分词时需要去除的停用词
② user_defined_words.txt
用来保存分词时用户自定义但分词程序无法识别的词语
③ weibo_uid.txt
由于本程序的设计是根据用户的uid进行微博内容的爬取，所以，用来保存需要爬取的足量的微博用户uid

2、weibo文件夹中的文件简介
① 每个txt文件以对应的微博用户id作为名称进行命名，文件中存储的内容是
从微博爬取的未经预处理的用户信息

② 用户微博内容的保存形式样例：
用户id: 1669879400
用户昵称：Dear-迪丽热巴
微博数: 964
关注数: 222
粉丝数: 62693922
原创微博内容: 
1:
2:
……

3、wei_user文件夹中的文件简介
① 每个txt文件以对应的微博用户id作为名称进行命名，文件中存储的内容是
从微博爬取的经过分词处理的用户信息
② 经分词处理的用户信息保存形式样例：


4、weiboJieba.py 用来完成分词处理的程序，并将结果保存于weibo_user文件夹下

5、weiboSpider.py 用来完成微博用户信息的爬取，并将结果保存于weibo文件夹下