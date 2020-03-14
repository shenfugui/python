# -*- ecoding: utf-8 -*-
# @ModuleName: d2
# @Function:
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 3/13/2020 11:29 AM

import requests
import time
import os
import threading
from lxml import etree
from queue import Queue


def get_urls(q, threads):
    # 解析得到图片地址
    url = 'https://www.27bao.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'Referer': 'https://www.27bao.com/'}
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    img_urls = html.xpath('/html/body/div[2]/div[1]/ul/li/a/img/@src')
    # 向队列中传入地址
    for url in img_urls:
        q.put(url)
    # 开启10个线程
    for i in range(10):
        t = threading.Thread(target=download, args=(url, q))
        t.start()
        threads.append(t)
    # 阻塞队列知直到队列为空
    q.join()
    # 向队列中传入None，通知队列退出
    for i in range(10):
        q.put(None)
    # 退出线程
    for thread in threads:
        thread.join()
    print('finished')


def download(url, q):
    # 从队列中取得图片地址
    while True:
        url = q.get()
        if url is None:
            break
    # 下载图片
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
    # 完成一个图片下载从队列删除该地址
        q.task_done()


def main():
    start = time.time()
    q = Queue()
    threads = []
    get_urls(q, threads)
    end = time.time()
    print('running %s s' % (end - start))


if __name__ == '__main__':
    main()
