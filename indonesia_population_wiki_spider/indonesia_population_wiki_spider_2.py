# -*- coding = utf-8 -*-
"""Wikipedia 印度尼西亚行政区与人口信息采集脚本。"""
# @Time: 2022/10/9 10:15
import sys

import requests
import random
import time
from lxml import etree
from urllib.parse import urljoin
import openpyxl


user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
]


def get_data(url):
    headers = {
        'user-agent': random.choice(user_agents),
    }
    for i in range(5):
        try:
            print(f'正在请求:{url}')
            res = requests.get(url, headers=headers, timeout=10)
            print(f'请求成功:{url}')
            time.sleep(random.uniform(0.5, 1) * 5)
            if res:
                return res
        except Exception as e:
            print(e)
            print(f'请求错误,正在进行第{i+1}次重试...')
            if i == 4:
                return None


def parse_first_data(first_res):
    # 使用xpath获取,每个地区
    tree = etree.HTML(first_res.text)
    hrefs = tree.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr/td[2]/a/@href')
    # print(len(hrefs))
    return hrefs


def parse_detail_res(res):
    tree = etree.HTML(res.text)
    tables = tree.xpath('//table')
    i = 0
    for table in tables:
        texts = table.xpath('.//tr/th//text()')
        for text in texts:
            if 'Area' in text:
                i += 1
        print(texts)
    print('i', i)
    return tables


def main():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '市/区'
    sheet['B1'] = '人口数量'
    i = 2
    # wb = openpyxl.load_workbook('人口数量.xlsx')
    # sheet = wb.active
    # i = 6307
    # 发送请求,获取第一页数据
    first_url = 'https://en.wikipedia.org/wiki/List_of_regencies_and_cities_of_Indonesia'
    first_res = get_data(first_url)
    if not first_res:
        wb.save('市区人口数量.xlsx')
        print('访问错误,终止程序!!!')
        sys.exit()
    # 解析数据
    hrefs = parse_first_data(first_res)
    # 获取514个县或市链接
    hrefs = hrefs[: -19]
    # hrefs = hrefs[100: 200]
    all_num = len(hrefs)

    for num, href in enumerate(hrefs):
        href = urljoin(first_url, href)
        print(f'开始访问第{num+1}个县或市,共有{all_num}个...')
        # href = 'https://en.wikipedia.org/wiki/Yahukimo_Regency'
        res = get_data(href)
        if not res:
            wb.save('市区人口数量.xlsx')
            print('访问错误,终止程序!!!')
            sys.exit()
        name = href.split('/')[-1].replace('_', ' ')
        tree = etree.HTML(res.text)
        tables = tree.xpath('//table')
        for table in tables:
            trs = table.xpath('.//tr')
            for tr_num, tr in enumerate(trs):
                th_text = tr.xpath('./th/text()')
                if th_text:
                    th_text = th_text[0]
                if th_text == 'Population':
                    # print(1, th_text)
                    th_text2 = trs[int(f'{tr_num+1}')].xpath(f'./th/text()')
                    if th_text2:
                        th_text2 = th_text2[0]
                        # print(th_text2)
                    if th_text2 == ' • Total':
                        total = trs[int(f'{tr_num+1}')].xpath(f'./td/text()')
                        if total:
                            total = total[0].replace(',', '')

                        print(name, total)

                        sheet[f'A{i}'] = name
                        sheet[f'B{i}'] = total
                        i += 1
    wb.save('市区人口数量.xlsx')


if __name__ == '__main__':
    main()

