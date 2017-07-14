import requests
import re
from bs4 import BeautifulSoup
res = requests.get('https://www.shiyanlou.com/courses/')#get请求，将结果保存到res中
soup = BeautifulSoup(res.text, 'lxml')#将结果中的html页面，让BeautifulSoup利用lxml解析，保存到soup中
course = soup.find_all('div',{'class':'col-md-4','class':'col-sm-6','class':'course'})#查找class为col-md-4 col-sm-6
for i in course:#循环从列表中，拿到每个课程的HTML代码
    title = i.find('div',{'class':'course-name'}).get_text()#获取课程标题
    study_people = i.find('span',{'class':'course-per-num','class':'pull-left'}).get_text()#获取课程的学习人数
    study_people = re.sub("\D", "", study_people)# 数字这里有太多的空格和回车，清理一下
    try:
        tag = i.find('span',{'class':'course-per-num','class':'pull-right'}).get_text()#查找课程类型，如果没有这行报错
    except:
        tag="课程"#上面报错，说明没有课程类型，只有普通课程没有，所以赋值课程
    print("{}    学习人数:{}    {}\n".format(tag, study_people,title,))#打印课程类型、学习人数、课程名
