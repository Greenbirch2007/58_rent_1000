#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://xa.58.com/yanta/chuzu/b2/?PGTID=0d3090a7-001e-77f5-7018-13cfa799e6d6&ClickID=2'
    driver.get(url)
    html = driver.page_source
    print(html)



get_first_page()


# 把首页和翻页处理？

def next_page():
    for i in range(1,71):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="bottom_ad_li"]/div[2]/a[last()]/span').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    jobs = selector.xpath("//div[@class='dw_table']/div/p/span[1]/a/@title")
    link = selector.xpath("//div[@class='dw_table']/div/p/span[1]/a/@href")
    firms = selector.xpath('//*[@id="resultList"]/div/span[1]/a/text()')
    long_tuple = (i for i in zip(jobs, link, firms))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into xian_python_link (jobs,link,firms) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





# if __name__ == '__main__':
#         html = get_first_page()
#         content = parse_html(html)
#         time.sleep(1)
#         insertDB(content)
#         while True:
#             html = next_page()
#             content = parse_html(html)
#             insertDB(content)
#             print(datetime.datetime.now())
#             time.sleep(1)


# # #
# create table xian_python_link(
# id int not null primary key auto_increment,
# jobs varchar(80),
# link varchar(88),
# firms varchar(80)
# ) engine=InnoDB  charset=utf8;



