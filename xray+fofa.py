import requests
import time
import base64
from urllib import request
import ssl
import os
from concurrent.futures import ThreadPoolExecutor


#api接口
url = 'https://api.fofa.so/v1/search'

headers = {
    #会员登录后获取Authorization（googl浏览器）
    'Authorization':'',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}
#搜索关键字
keyword = 'country="CN"&& discuz'
b64_keyword =  str(base64.b64encode(keyword.encode('utf-8')),'utf-8')

def spider(surl):
    total = 0
    #set数据类型能去重
    url_lst = set()
    #设置爬取页码
    for i in range(1,1001):
        print('当前爬取第{}页'.format(str(i)))
        print("当前的爬取的url总数为：{}".format(str(len(url_lst))))
        params = {
            'q': keyword,
            'qbase64': b64_keyword,
            'full': 'false',
            'pn': i,
            'ps': 10
        }
        try:
            resp = requests.get(surl,params=params,headers=headers,timeout=10)
            print(resp.text)
            for i in range(10):
                #解析json数据中的host
                url = resp.json()['data']['assets'][i]['link']
                url_lst.add(url)
                print(url)
            time.sleep(2)
        except:
            continue
    return url_lst

#存活验证
def check_url(url,total):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    try:
        #添加去除ssl验证
        context = ssl._create_unverified_context()

        req = request.Request(url, headers=headers)
        resp = request.urlopen(req,timeout=6,context=context)
        print(resp.code)
        if resp.code == 200 and 'edu' not in url:
            print("已经验证的网址总量是 ：{}".format(str(len(total)+1)))
            print("当前验证的网址是：{}".format(url))
            print('*' * 20)
            total.add(url)
            #写入文件
            with open('discuz.txt', 'a') as f1:
                f1.write(url+"\n")
            time.sleep(1)
            resp.close()
        else:
            time.sleep(1)
            resp.close()
    except:
        return

def main(urls):
    #开启线程池
    with ThreadPoolExecutor(50) as t:
        total = set()
        for url in urls:
            #添加线程的延迟，去掉可能因为并发过多，产生timeout异常
            if (len(total)+1)%15 ==0:
                time.sleep(3)
            t.submit(check_url,url=url,total=total)
    print(total)

def xray(file='churls.txt'):
    with open(file,'r') as f:
        urls = f.readlines()
        num = 1
        for url in urls:
            name = './edu/'+str(num)+'.'+url.split('//')[1].strip()+'.html'
            os.system("xray_windows_amd64.exe webscan --basic-crawler {}  --html-output {}.html".format(url.strip(),name))
            # print("xray_windows_amd64.exe webscan --basic-crawler {} --html-output {}.html".format(url.strip(),name))
            num += 1
            time.sleep(1)

if __name__ == '__main__':
    url_lst = spider(url)
    #可以去掉提取的url_lst的显示
    print(url_lst)
    main(url_lst)
    # xray()
