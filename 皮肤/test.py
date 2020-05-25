# -*- ecoding: utf-8 -*-
# @ModuleName: test
# @Function:
# @Author: shenfugui
# @Email: shenge_ziyi@163.com
# @Time: 3/13/2020 10:40 PM

import threading
import requests
import time
import os
import json
from queue import Queue


class my_thread(threading.Thread):
    def __init__(self, headers, q):
        threading.Thread.__init__(self)
        self.headers = headers
        self.q = q

    def run(self):
        get_imgs(self.headers, self.q)


def get_heros(headers, q, threads):
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    data = json.loads(r.text)
    for hero in data['hero']:
        id = hero['heroId']
        q.put(id)
    for i in range(100):
        t = my_thread(headers, q)
        t.start()
        threads.append(t)
    q.join()
    for i in range(100):
        q.put(None)
    for thread in threads:
        thread.join()
    print('finished')


def get_imgs(headers, q):
    while True:
        id = q.get()
        if id is None:
            break
        try:
            url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(
                id)
            r = requests.get(url, headers=headers, timeout=10)
            r.encoding = r.apparent_encoding
            data = json.loads(r.text)
            for skin in data['skins']:
                hero_name = './' + skin['heroName']
                skin_url = skin['mainImg']
                skin_name = skin['name'].replace('/', '')
                if not os.path.exists(hero_name):
                    os.mkdir(hero_name)
                pic = requests.get(skin_url, headers=headers)
                with open(hero_name + '/' + skin_name + '.jpg', 'wb') as f:
                    f.write(pic.content)
                    print('%s 下载成功' % (skin_name))
        except requests.exceptions.ConnectionError:
            time.sleep(5)
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidSchema:
            pass
        q.task_done()


def main():
    start = time.time()
    q = Queue()
    threads = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
               'Connection': 'close'}
    get_heros(headers, q, threads)
    end = time.time()
    print('共用时%s s' % (end - start))


if __name__ == '__main__':
    main()
