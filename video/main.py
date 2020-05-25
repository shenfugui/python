import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_urls(number):
    url = 'https://www.hs684.com/Html/60/index-%d.html'%number
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'lxml')
    lists = soup.find('ul',class_ = 'towmd ttss1 videolist').find_all('li')
    data = []
    for list in lists:
        link = 'https://www.hs053.com%s'%list.a['href']
        data.append(link)
    return data

def get_video_urls(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    video_urls = soup.find(id = 'http_down_url')['href']
    download(video_urls)

def download(url):
    r = requests.get(url,stream=True)
    with open('./{}'.format(url.split('/')[-1]),'wb') as f:
        f.write(r.content)

def main():
    number = 1
    while (number <= 99):
        for url in get_urls(number):
            # print(url)
            get_video_urls(url)
        number += 1

if __name__ == '__main__':
    main()
