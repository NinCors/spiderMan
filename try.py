from try_sql import insertData
import requests
import re
from bs4 import BeautifulSoup
import time

course_count = 0
study_num = 0

host_url = "http://www.shiyanlou.com{}"

def write_file(string):
    log = open("data.log",'a')
    log.write(string + '/n')
    log.close()


def parse_content(url,title,tag,study_num):
    print(url,'&'*10)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    type_list = soup.select('ol[class=breadcrumb] > li > a')
    # check ol -> li -> a tag. Get the info
    types = []
    for i in type_list:
        if (type_list.index(i) != 0) and (type_list.index(i) != len(type_list) - 1):
            types.append(i.get_text())
    info = soup.find('div',{'class':'course-infobox-content'})

    try:
        info = info.find('p').get_text()
    except:
        info = "Nothing"

    teacher = soup.find('div',{'class':'name'})
    try:
        teacher = teacher.find('strong').get_text()
    except:
        teacher = "unknown"

    labs = soup.find('div',{'id':'labs'})
    test_list = labs.find_all('div',{'class':'lab-item'})
    tests_name = []
    for i in test_list:
        name = i.find('div',{'class':'lab-item-title'}).get_text()
        tests_name.append(name)
    write_file("Class: {} Teacher: {} Tag: {} NumStudied: {} Type: {}".format(title,teacher,tag,study_num,'&'.join(types)))
    write_file("Intro: {}".format(info))
    for i in tests_name:
        write_file(i)
    write_file('*'*100)
    # insert it into database
    print(url,insertData(url, title, teacher, study_num, tag, '-'.join(types), info, '-'.join(tests_name)))


def get_course_link(url):
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    course = soup.find_all('div', {'class': 'col-md-4', 'class': 'col-sm-6', 'class': 'course'})
    for i in course:
        href = i.find('a',{'class':'course-box'}).get('href')#获取课程的链接，进入课程详情页面
        title = i.find('div', {'class': 'course-name'}).get_text()#获取课程名
        study_people = i.find('span', {'class': 'course-per-num', 'class':'pull-left'}).get_text()#获取学习人数
        study_people = re.sub("\D", "", study_people)  #数字这里有太多的空格和回车，清理一下
        try:#查询课程类型，普通课程则没有，用try
            tag = i.find('span', {'class': 'course-per-num','class': 'pull-right'}).get_text()
        except:
            tag = "课程"
        parse_content(url=host_url.format(href),title=title,tag=tag,study_num=study_people)#将数据丢到下一个函数
        time.sleep(0.5)#睡眠0.5秒，防止太快

def main():
    res = requests.get('https://www.shiyanlou.com/courses/')#发起get将结果保存到res中
    soup = BeautifulSoup(res.text, 'lxml')
    course_link ="https://www.shiyanlou.com/courses/?course_type=all&tag=all&fee=all&page={}"#课程的链接都是这样的格式，首先定义好
    page = soup.find_all('ul',{'class':'pagination'})#获取底部导航栏的全部信息
    if len(page)<1:#判断，如果没拿到，爬虫无法继续，中断操作
        print('未获得全部页面')
        return None
    li_num = page[0].find_all('li')#查询底部li，因为数据保存在li中
    page_num = 0#首先设定page_num=0，页面数据肯定是大于0的
    for i in li_num:
        try:
            li_num = int(i.find('a').get_text())#获取放在a标签的字符串数字，并用int强制转换
        except:
            li_num = 0#如果获取失败，则赋值0
        if li_num > page_num:#page_num永远保存最大的值
            page_num = li_num
        # print(page_num,type(page_num))
    for i in range(1,page_num+1):#拿到page_num数字，从1开始数到page_num
        get_course_link(course_link.format(i))

if __name__ == "__main__":
    main();
    print("Total class: {}   time studied: {}".format(course_count,study_num))
