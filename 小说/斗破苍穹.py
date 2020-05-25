# -*- ecoding: utf-8 -*-
# @ModuleName: 斗破苍穹
# @Function:
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 2020/3/16 10:43

import requests
import time
import os
import threading
from lxml import etree
from queue import Queue


class Mythreads(threading.Thread):
    def __init__(self, headers, q1, q2):
        threading.Thread.__init__(self)
        self.headers = headers
        self.q1 = q1
        self.q2 = q2

    def run(self):
        get_text(self.headers, self.q1, self.q2)


def get_urls(headers, q1, q2, threads):
    url = 'http://www.tycqxs.com/57_57672/'
    r = requests.get(url, headers=headers,timeout=10)
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    urls = html.xpath('//*[@id="list"]/dl/dd[9]/following-sibling::dd/a/@href')
    titles = html.xpath('//*[@id="list"]/dl/dd[9]/following-sibling::dd/a/text()')
    for url in urls:
        content_url = 'http://www.tycqxs.com/' + url
        q1.put(content_url)
    for title in titles:
        content_title = title
        q2.put(content_title)
    for i in range(10):
        t = Mythreads(headers, q1, q2)
        t.start()
        threads.append(t)
    q1.join()
    q2.join()
    for i in range(10):
        q1.put(None)
        q2.put(None)
    for t in threads:
        t.join()
    print('finished')


def get_text(headers, q1, q2):
    while True:
        url = q1.get()
        title = q2.get()
        if url is None:
            break
        try:
            r = requests.get(url, headers=headers,timeout=10)
            r.encoding = r.apparent_encoding
            html = etree.HTML(r.text)
            contents = html.xpath('//*[@id="content"]/br/text()')
            path = './novel/'
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path + title + '.txt', 'a', encoding='utf-8') as f:
                for content in contents:
                    f.write(content)
            print('%s 下载完成' % title)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ReadTimeout:
            pass
    q1.task_done()
    q2.task_done()


def main():
    start = time.time()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Connection': 'closed'}
    q1 = Queue()
    q2 = Queue()
    threads = []
    get_urls(headers, q1, q2, threads)
    end = time.time()
    print('running %s s' % (end - start))


if __name__ == '__main__':
    main()
