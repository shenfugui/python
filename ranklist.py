# -*- coding: utf-8 -*-
# @Time    : 2020/3/11 23:00
# @Author  : shenfugui
# @Email   : shenge_ziyi@163.com
# @File    : ranklist.py

import requests
import csv
from bs4 import BeautifulSoup

def getlist(number):
    url = 'https://maoyan.com/board/4?offset=%d'%number
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Referer': 'https: // maoyan.com / board'
    }
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'html.parser')
    dds = soup.find('dl',class_ = 'board-wrapper').find_all('dd')
    with open('./list.csv', 'a') as f:
        fieldnames = ['电影名称', '主演', '上映时间']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dd in dds:
            title = dd.a['title']
            stars = dd.find('p',class_ = 'star').get_text()
            time = dd.find('p',class_ = 'releasetime').get_text()
            writer.writerow({'电影名称':title,'主演':stars,'上映时间':time})
            
def main():
    number = 0
    while (number <= 90):
        getlist(number)
        number += 10

if __name__ == '__main__':
    main()

