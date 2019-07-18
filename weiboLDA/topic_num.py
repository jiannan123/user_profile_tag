import numpy
import math
import string
import matplotlib.pyplot as plt
import os
import traceback

def dictionary_found(wordlist):               #对模型训练出来的词转换成一个词为KEY,概率为值的字典。
    word_dictionary1= {}
    for i in range(len(wordlist)):
        if i%2==0:
            if word_dictionary1.__contains__(wordlist[i])==True:
                word_probability=word_dictionary1.get(wordlist[i])
                word_probability=float(word_probability)+float(wordlist[i+1])
                word_dictionary1.update({wordlist[i]:word_probability})
            else:
                word_dictionary1.update({wordlist[i]:wordlist[i+1]})
        else:
            pass
    return word_dictionary1

def look_into_dic(dictionary,testset):          #对于测试集的每一个词，在字典中查找其概率。
    '''Calculates the TF-list for perplexity'''
    frequency=[]
    letter_list=[]
    a=0.0
    for letter in testset.split():
        if letter not in letter_list:
            letter_list.append(letter)
            letter_frequency=(dictionary.get(letter))
            frequency.append(letter_frequency)
        else:
            pass
    for each in frequency:
        if each!=None:
            a+=float(each)
        else:
            pass
    return a


def f_testset_word_count(testset):                                     #测试集的词数统计
    '''reture the sum of words in testset which is the denominator of the formula of Perplexity'''
    testset_clean=testset.split()
    return (len(testset_clean)-testset.count("\n"))

def f_perplexity(word_frequency,word_count):             #计算困惑度
    '''Search the probability of each word in dictionary
    Calculates the perplexity of the LDA model for every parameter T'''
    duishu=-math.log(word_frequency)
    kuohaoli=duishu/word_count
    perplexity=math.exp(kuohaoli)
    return perplexity

def graph_draw(topic,perplexity):             #做主题数与困惑度的折线图
    x=topic
    y=perplexity
    plt.plot(x,y,color="red",linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()


topic = []
perplexity_list = []
file_dir = "D:\\py_practice\\weiboSpider"
file_path1 = "D:\\py_practice\\weiboSpider\\all\\all.txt"
f1 = open(file_path1, 'r',encoding="utf-8")      #测试集目录
testset = f1.read()
testset_word_count=f_testset_word_count(testset)         #计算测试集中的单词总数
for root, dirs, files in os.walk(file_dir + os.sep + "weibo_user"):
    for file in files:
        try:
            dictionary = {}
            topic.append(file)  # 模型文件名的迭代公式
            file_path2 = file_dir + os.sep + "weibo_user" + os.sep + file  # 模型目录
            f = open(file_path2, 'r', encoding="utf-8")
            text = f.readlines()
            word_list = []
            for line in text:
                if "Topic" not in line:
                    line_clean = line.split()
                    word_list.extend(line_clean)
                else:
                    pass
            word_dictionary = dictionary_found(word_list)
            frequency = look_into_dic(word_dictionary, testset)
            perplexity = f_perplexity(frequency, testset_word_count)
            perplexity_list.append(perplexity)
            topic.append(file)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
graph_draw(topic,perplexity_list)
