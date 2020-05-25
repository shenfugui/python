# -*- ecoding: utf-8 -*-
# @ModuleName: novel
# @Function:
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 3/13/2020 3:36 PM

import requests
import os
import time
import threading
from lxml import etree
from queue import Queue
from bs4 import BeautifulSoup

# 获取每个章节小说地址


def get_urls(headers,threads,q):
    url = 'http://www.ishisetianxia.com/chaojishenxiang/'
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    urls = html.xpath('/html/body/div[3]/div[3]/dl/dd/a/@href')
    for url in urls:
        n_url = 'http://www.ishisetianxia.com/' + url
        q.put(n_url)
    for i in range(10):
        t = threading.Thread(target=download_novel,args=(headers,q))
        t.start()
        threads.append(t)
    q.join()
    for i in range(10):
        q.put(None)
    for t in threads:
        t.join()
    print('finished')

# 下载小说


def download_novel(headers,q):
    while True:
        # 阻塞直到从队列获取一条消息
        url = q.get()
        if url is None:
            break
        try:
            r = requests.get(url, headers=headers,timeout=10)
            r.encoding = r.apparent_encoding
            path = './novel/'
            if not os.path.exists(path):
                os.mkdir(path)
            soup = BeautifulSoup(r.text,'lxml')
            title = soup.find('div',class_="inner").h1.get_text()
            contents = soup.find('div',id="BookText").find_all('p')
            n_path = path + title + '.txt'
            with open(path + title + '.txt', 'a', encoding='utf-8') as f:
                for content in contents:
                    f.write(content.get_text())
            print('%s 下载完成' % title)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        q.task_done()


def main():
    start = time.time()
    q = Queue()
    threads = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'Connection': 'close'}
    get_urls(headers,threads,q)
    end = time.time()
    print('共用时%s s' % (end - start))


if __name__ == '__main__':
    main()
