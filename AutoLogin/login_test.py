from time import sleep

import requests
import json
from os import system
from requests.cookies import cookiejar_from_dict

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

def loadConfig(param):
    # 读取参数
    key = 'id' if param.isdigit() else 'domain'
    try:
        if key:
            with open('login_config.json', encoding='utf-8-sig')as j:
                config_list = json.load(j)
                for config in config_list:
                    if str(config[key]) == param:
                        return config
                system('不存在该登录信息')
    except:
        raise Exception

def doLogin(config):
    # 登录
    request_config = config['request']
    cookie_jar = cookiejar_from_dict({})
    s = requests.session()
    for request in request_config:
        sleep(2)
        step = request['step']
        req_type = request['type']
        url = request['url_request']
        data = request['data']
        print(f'正在执行第{step}步...请求{url}')
        try:
            if req_type == 'post':
                r = s.post(url=url, data=data, cookies=cookie_jar)
            else:
                r = s.get(url=url, data=data, cookies=cookie_jar)
            if r.ok:
                cookie_jar = r.cookies
        except Exception as e:
            raise Exception
            # print(f'login failed\n{repr(e)}')
    return cookie_jar

def loginCheck(cookie, config):
    # 校验Cookie是否有效
    url_check = config['url_check']
    re_check = config['re_check']
    try:
        r = requests.get(url=url_check, cookies=cookie)
        if r.ok:
            html = r.text
            flag = html.find(re_check)
            print(flag)
            if flag != -1:
                print('登录成功')
                return True
            print('登录失败')
        else:
            raise ConnectionError
    except Exception as e:
        print(f'check failed\n{repr(e)}')

def main():
    
    param = input('查询参数：')
    config = loadConfig(param)
    cookie = doLogin(config)
    loginCheck(cookie, config)

if __name__ == "__main__":
    main()
