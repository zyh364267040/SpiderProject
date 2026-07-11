# -*- coding = utf-8 -*-
# @Time: 2022/10/17 17:13
import requests
import openpyxl
import time
import random
import os
import sys

from browser_cookie_refresh_helper import control


def get_data(url, done_list, cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'cookie': cookie
    }
    for i in range(5):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            time.sleep(random.choice([9, 10, 11, 12]))
            if res and res.status_code == 200:
                print(f'请求成功:{url}')
                return res
            else:
                print(f'请求失败:{url}')
        except Exception as e:
            print(url)
            print('出错了,正在重试...', e)


def parse_data(res, done_list, name):
    try:
        res_dic = res.json()
        for k, v in res_dic.items():
            with open('done.csv', 'a', encoding='utf-8') as f:
                print(f"{name}, {k}, {v['inventory']}")
                f.write(f"{name}, {k}, {v['inventory']}\n")
        done_list.append(name)
        print(f'{name}保存成功!')
    except Exception as e:
        print('解析数据,发生错误:', e)


def main(cookie):
    # 1. 读取excel
    wb = openpyxl.load_workbook('products.xlsx')
    sheet = wb.active
    row = sheet.max_row

    # 2. 已完成列表
    done_list = []

    # 3. 判断保存表格是否存在
    if os.path.exists('done.csv'):
        with open('done.csv', 'r', encoding='utf-8') as f:
            for name in f.readlines()[1:]:
                name = name.split(', ')[0]
                if name in done_list:
                    continue

                # 将已经获取的数据型号名添加到去重列表中
                done_list.append(name)
    else:
        with open('done.csv', 'w', encoding='utf-8') as f:
            f.write(f'型号, 型号名称, 数量\n')

    # 4. 逐条取出每一个
    for i in range(1, row+1):
        name = sheet[f'A{i}'].value
        if name in done_list:
            continue

        print(f'开始第{i}个,共有{row}个.')

        # 5. 发送请求,获取响应
        # url = f'https://www.ti.com.cn/productmodel/gpn/{name}/tistoresegmented'
        url = f'https://www.ti.com/productmodel/gpn/{name}/tistoresegmented'
        res = get_data(url, done_list, cookie)

        # 6. 解析数据
        if res:
            parse_data(res, done_list, name)
        else:
            print(i)
            break


if __name__ == '__main__':
    while True:
        cookie = input('请输入cookie:')
        # cookie = cookie.split(': ')[-1]
        main(cookie)
        time.sleep(60)
        control()
