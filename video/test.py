import requests

def get():
    url  = 'https://d.sh026.com/20200303/109/1091/1091.mp4'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Host': 'www.hs053.com'
    }
    r = requests.get(url,headers=headers,stream = True)
    print(r.status_code)
    with open('./1.mp4','wb') as f:
        f.write(r.content)
get()