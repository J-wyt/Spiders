# encoding: utf-8
__author__ = 'Jeremiah'

import requests
import re
from time import time, sleep

HEADERS = {
    'referer': 'https://cn.bing.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}


URL = f'https://cn.bing.com/HPImageArchive.aspx?format=js&n=1&nc={int(time()*1000)}&pid=hp&idx='
img_infos = []
regex = re.compile('\\"enddate\\":\\"(\d+)\\",\\"url\\":\\"([^"]+)\\".*?\\"copyright\\":\\"([^"]+)\\"')
path = 'C:\\Users\\Administrator\\Pictures'

def get_img_url(num):
    for i in range(0, num):
        sleep(1)
        try:
            r = requests.get(url=URL+str(i), headers=HEADERS, timeout=5)
            if r.ok or r.status_code == 200:
                img_info = regex.findall(r.text)[0]
                img_infos.append(img_info)
            else:
                raise ConnectionError
        except Exception as e:
            print(f'获取链接失败，{repr(e)}')

def download(img_info):
    global path
    url = f'https://cn.bing.com{img_info[1]}'
    date = img_info[0]
    name = img_info[2].replace('/','-')
    try:
        sleep(1)
        r = requests.get(url=url, headers=HEADERS, timeout=10)
        if r.ok or r.status_code == 200:
            print(f'正在下载bing壁纸。。。{name}')
            with open(f'{path}\\{date}_{name}.jpg', 'wb')as f:
                f.write(r.content)
        else:
            raise ConnectionError
    except Exception as e:
        print(f'下载图片失败，{repr(e)}')

def main():
    get_img_url(1)
    for img_info in img_infos:
        download(img_info)

if __name__ == '__main__':
    main()
