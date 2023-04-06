import re
import json
import time


def main():
    with open('amzn.html', 'r', encoding='utf-8') as f:
        res = f.read()
        print(res)
    # 使用正则获取reviews
    pattern = r',"reviews":(.*?)},"fe'
    reviews = re.findall(pattern, res)[0]
    reviews = json.loads(reviews)
    print(reviews)


def read_txt():
    f_r = open('company_info.txt', 'r', encoding='utf-8')
    lines = f_r.readlines()
    if len(lines) < 16:
        print('company_info.txt文件请求内容为空!!!')
        # break
    if not lines[15]:
        print('company_info.txt文件17行没有内容!!!')
        # break
    info = lines[15]
    f_r.close()

    print(1)
    time.sleep(20)
    print(2)

    f_w = open('company_info.txt', 'w+', encoding='utf-8')
    lines = f_r.readlines()
    for line in lines:
        if info in line:
            continue
        f_w.write(line)
    f_w.close()


if __name__ == '__main__':
    read_txt()
