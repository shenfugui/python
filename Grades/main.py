import requests
from bs4 import BeautifulSoup


def login():
    data = {
        'userAccount': '201905165028',
        'userPassword': '',
        'encoded': '2Bm06179090P5271lL26E50045255L88Nc%257fm%25e8%252s9hJ8e5Gn97g7Ue666.'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Referer': 'http://bkjx.wust.edu.cn/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    url = 'http://bkjx.wust.edu.cn/Logon.do?method=logon'

    sessions = requests.session()

    response = sessions.post(url, headers=headers, data=data)

    if (response.status_code == 200):
        get_list()
    else:
        print('login error')


def get_list():
    url = 'http://bkjx.wust.edu.cn/jsxsd/kscj/cjcx_list'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'http://bkjx.wust.edu.cn/jsxsd/kscj/cjcx_query',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Cookie': 'JSESSIONID=E5EE266AC85F663C14709E6C2629958C; Hm_lvt_be5a5579e213a62e5322030a519a9123=1589964243; JSESSIONID=7E39A1A3CA3400555D00C2F31FF2E363; SERVERID=129'
    }

    data = {
        'kksj': '',
        'kcxz': '',
        'kcmc': '',
        'xsfs': 'all'
    }

    response = requests.post(url, headers=headers, data=data)

    if (response.status_code == 200):
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'lxml')
        lessons = soup.find('table',id='dataList').find_all('th')
    else:
        print('Couldn\'t get list')


def main():
    login()


if __name__ == '__main__':
    main()
