# -*- coding: utf-8 -*-
"""Google Patents 专利搜索结果链接采集脚本。

根据关键词和语言条件请求 Google Patents 搜索接口，解析专利详情页链接并写入文本文件。
"""
# @Time: 2022/9/24 20:19
import requests
import re
import json
from urllib.parse import urljoin
import time
import random


def get_data(url, page):
    # headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    # 参数
    params = {
        'url': f'q=(fintech)&language=CHINESE&num=100&oq=(fintech)+language:+Chinese&page={page}',
        'exp': '',
        'tags': ''
    }
    # 发送请求
    res = requests.get(url, headers=headers, params=params)
    return res


def parse_and_save_data():
    # 创建文件
    with open('google.txt', 'a', encoding='utf-8') as f:
        url = 'https://patents.google.com/xhr/query'
        # 循环请求每一页
        page = 0
        while True:
            # 判断页码
            if page > 9:  # 4831条,每页100条,一共49页,从0开始,page到48
                break
            # 发送请求获取响应
            res = get_data(url, page)
            print(res.text)
            # print(res.text)
            # 使用正则获取数据
            pattern = r'"result":(.*?)}], "chem_exhausted"'
            data_str = re.findall(pattern, res.text)[0]

            # 把获得的字符串转成json
            data_json_list = json.loads(data_str)
            # print(len(data_json_list))
            for data_json in data_json_list:
                detail_url = data_json['id']
                detail_url = 'https://patents.google.com/' + detail_url
                # 写入文件
                f.write(detail_url + '\n')
                print(detail_url)

            page += 1
            time.sleep(random.choice([2, 3, 4]))


def main():
    parse_and_save_data()


if __name__ == '__main__':
    main()
