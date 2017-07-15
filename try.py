import requests
import re
from bs4 import BeautifulSoup

course_count = 0
study_num = 0

def getCourse(url):
    res = requests.get(url)#get请求，将结果保存到res中
    soup = BeautifulSoup(res.text, 'lxml')#将结果中的html页面，让BeautifulSoup利用lxml解析，保存到soup中
    course = soup.find_all('div',{'class':'col-md-4','class':'col-sm-6','class':'course'})#查找class为col-md-4 col-sm-6
    for i in course:#循环从列表中，拿到每个课程的HTML代码
        global course_count
        global study_num
        course_count = course_count + 1
        title = i.find('div',{'class':'course-name'}).get_text()#获取课程标题
        study_people = i.find('span',{'class':'course-per-num','class':'pull-left'}).get_text()#获取课程的学习人数
        study_people = re.sub("\D", "", study_people)# 数字这里有太多的空格和回车，清理一
        study_num = study_num + int(study_people)
        try:
            tag = i.find('span',{'class':'course-per-num','class':'pull-right'}).get_text()#查找课程类型，如果没有这行报错
        except:
            tag="课程"#上面报错，说明没有课程类型，只有普通课程没有，所以赋值课程
        print("{}    学习人数:{}    {}\n".format(tag, study_people,title,))#打印课程类型、学习人数、课程名i


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
        getCourse(course_link.format(i))

if __name__ == "__main__":
    main();
    print("Total class: {}   time studied: {}".format(course_count,study_num))
