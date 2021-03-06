import requests
import csv
import time
import threading
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
    start = time.time()
    number = 0
    while (number <= 90):
        t = threading.Thread(target=getlist,args=(number,))
        t.start()
        t.join()
        number += 10
    end = time.time()
    print('running %s s'%(end-start))

if __name__ == '__main__':
    main()

