# -*- coding = utf-8 -*-
# @Time: 2022/10/16 22:06
import requests
import time
import random
import openpyxl


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    for i in range(10):
        try:
            res = requests.get(url, headers=headers)
            time.sleep(random.choice([2, 3, 4]))
            if res and res.status_code == 200:
                print(f'请求成功:{url}')
                return res
            else:
                print('获取数据失败!')
        except Exception as e:
            print(url)
            print('出错了,正在重试...', e)
            if i == 9:
                with open('shibai.txt', 'w', encoding='utf-8') as f:
                    f.write(url + '\n')


def main():
    url = ''
    get_data(url)

    name_list = []

    with open('name.csv', 'r', encoding='utf-8') as f:
        for name in f.readlines():
            if name:
                name = name.replace(',', '').strip()
                print(name)
                if name in name_list:
                    continue
                name_list.append(name)

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '型号名称'
    i = 2

    for name in name_list:
        sheet[f'A{i}'] = name
        i += 1

    wb.save('ti.xlsx')


if __name__ == '__main__':
    main()
