# -*- ecoding: utf-8 -*-
# @ModuleName: download_imgs
# @Function: 
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 3/13/2020 11:29 AM

import requests
import time
import os
from lxml import etree

#解析网页，获取动图的地址
def get_urls():
    url = 'https://www.27bao.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'Referer': 'https://www.27bao.com/'}
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    img_urls = html.xpath('/html/body/div[2]/div[1]/ul/li/a/img/@src')
    for url in img_urls:
        download(url)


#下载动图
def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'Referer': 'https://www.27bao.com/'}
    r = requests.get(url, headers=headers)
    path = './imgs/'
    if not os.path.exists(path):
        os.mkdir(path)
    img_path = path + url.split('/')[-1] + '.gif'
    with open(img_path, 'wb') as f:
        f.write(r.content)
        print('success')


def main():
    start = time.time()
    get_urls()
    end = time.time()
    print('running %s s' % (end - start))


if __name__ == '__main__':
    main()
