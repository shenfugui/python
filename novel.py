import requests
from bs4 import BeautifulSoup

def get_urls():
    url = 'http://www.xbiquge.la/14/14930/'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'lxml')
    lists = soup.find('div',id = 'list').find_all('dd')
    for list in lists:
        url = 'http://www.xbiquge.la/' + list.a['href']
        download(url)

def download(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'lxml')
    title = soup.find('div',class_ = 'bookname').find('h1').get_text()
    name = title + '.txt'
    content = soup.find('div',id = 'content').get_text()
    with open(name,'w',encoding='utf-8') as f:
        f.write(content)
    print("正在下载%s" % title)

def main():
    get_urls()

if __name__ == '__main__':
    main()
