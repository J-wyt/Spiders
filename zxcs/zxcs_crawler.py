# author: Jeremiah
# date: 2018/9/3

import requests
import argparse
import winreg
from lxml import etree

HEADERS = {
    'Referer': 'http://www.zxcs8.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

URL = 'http://www.zxcs8.com/index.php'

VERSION = 'VERSION 0.0.1'

def getParser():  
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='知轩藏书小说下载器')
    parser.add_argument('keyword', metavar="KEYWORD", type=str, nargs="*", help='novel keyword.')
    parser.add_argument('-v', '--version', action='store_true', help='version information.')
    return parser

def cliRun():
    # 执行命令行操作
    parser = getParser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)
        return
    
    if not(args['keyword']):
        parser.print_help()
    
    else:
        run(args['keyword'][0])
        

def getDesktop():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, 
        r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    )
    return winreg.QueryValueEx(key, "Desktop")[0]

def getDownUrl(name):
    # 获取rar下载链接
    try:
        # 第一层
        r1 = requests.get(URL, params={'keyword': name}, headers=HEADERS, timeout=20)
        print(f'正在搜索：{name}...')
        target = etree.HTML(r1.content).find('.//dl[@id="plist"]/dt/a')
        print(f'找到：{target.text}')
        # 第二层
        r2 = requests.get(target.get('href').replace('post/', 'download.php?id='), headers=HEADERS)
        file_info = etree.HTML(r2.content).find('.//span[@class="downfile"]/a')
        return (name, file_info.get('href'))
    except Exception as e:
        print(f'获取下载链接失败！\n错误原因：{repr(e)}')

def download(info):
    # 下载
    file_name = info[0]
    file_url = info[1]
    try:
        r = requests.get(file_url, headers=HEADERS, stream=True, timeout=20)
        if r.status_code == 200:
            # download start
            file = f'{getDesktop()}\\{file_name}.rar'
            print(f'开始下载...{file}')
            with open(file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            print('下载完成！')
    except Exception as e:
        print(f'下载文件失败！\n错误原因：{repr(e)}')


def run(name):
    info = getDownUrl(name)
    download(info)

if __name__ == '__main__':
    cliRun()
