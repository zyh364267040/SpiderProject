# -*- coding = utf-8 -*-
# @Time: 2022/10/16 14:11
"""多来源药品公开信息采集脚本。

从 RxList 获取药品条目与说明内容，结合 DrugFuture 和药智网补充规格及企业信息。
"""
import requests
import time
import random
from lxml import etree
import openpyxl
from urllib.parse import urljoin
import os


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
                with open('shibai.txt', 'a', encoding='utf-8') as f:
                    f.write(url + '\n')


def post_data(name):
    url = 'https://www.drugfuture.com/fda/drugsearch.aspx'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    data = {
        'SearchTerm': name,
        'SearchType': 'BasicSearch',
        'submit': '查询'
    }
    for i in range(10):
        try:
            res = requests.post(url, headers=headers, data=data)
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
                with open('shibai.txt', 'a', encoding='utf-8') as f:
                    f.write(url + '\n')


def parse_data(res):
    # 使用xpath解析数据
    tree = etree.HTML(res.text)
    li_list = tree.xpath('//*[@id="search"]/section/article/div[2]/ul/li')
    return li_list


def parse_detail_data(res):
    # 使用xpath解析数据
    tree = etree.HTML(res.text)
    sections = tree.xpath('/html/body/main/section/article/div/section')
    p_text = sections[1].xpath('./div/div/div[2]/p[1]/text()')
    if p_text:
        p_text = p_text[0]
    else:
        p_text = ''
    ul_text_list = sections[1].xpath('./div/div/div[2]/ul//text()')
    if ul_text_list:
        for ul_text in ul_text_list:
            p_text += ul_text.strip().replace('\n', '').replace('\r', '')

    return p_text


def save_data():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '药品名称'
    sheet['B1'] = '辅料'
    sheet['C1'] = '适应症'
    sheet['D1'] = '处方组成'
    sheet['E1'] = '规格'
    sheet['F1'] = '企业名称'
    sheet['G1'] = '药代动力学参数'
    sheet['H1'] = '熔点'
    i = 2


def parse_guige_data(res):
    # 解析规格数据
    tree = etree.HTML(res.text)
    guige_list = tree.xpath('/html/body/div[4]/table/tbody/tr/td[7]/text()')
    if guige_list:
        guige = guige_list[0]
    else:
        guige = ''
    return guige


def parse_company(res):
    tree = etree.HTML(res.text)
    company_list = tree.xpath('//table/tbody/tr[1]/td[6]/text()')
    if company_list:
        company = company_list[0]
    else:
        company = ''
    return company


def main():
    done_list = []

    if os.path.exists('yao.csv'):
        with open('yao.csv', 'r', encoding='utf-8') as f:
            for name in f.readlines():
                name = name.split(',')[0]
                done_list.append(name)
    # 1. 发送请求,获取起始数据
    url = 'https://www.rxlist.com/search/rxl/soft%20capsule'
    res = get_data(url)

    # 2. 解析数据
    li_list = parse_data(res)

    # 3. 循环取出每一个药品,进行请求,获取数据
    for li in li_list:
        name = li.xpath('./a/span[1]/text()')[0].split(': ')[-1]
        href = li.xpath('./a/@href')[0]
        if name in done_list:
            continue
        if name and href:
            href = urljoin(url, href)
            # href = 'https://www.rxlist.com/nalfon-drug.htm#indications'
            res = get_data(href)

            if res:
                # 4. 解析药品数据
                # p_text 处方组成
                p_text = parse_detail_data(res)

                # 5. 获取药品规格
                res = post_data(name)
                if res:
                    guige = parse_guige_data(res)

                    # 6. 获取企业名称
                    name = name.replace(' ', '+')
                    url = f'https://db.yaozh.com/fdalabel?comprehensivesearchcontent={name}'
                    name = name.replace('+', ' ')
                    res = get_data(url)
                    if res:
                        company = parse_company(res)

                        name = name.replace(',', '.')
                        p_text = p_text.replace(',', '.').replace('\n', '')
                        guige = guige.replace(',', '.')
                        company = company.replace(',', '.')

                        print('name', name)
                        print('p_text', p_text)
                        print('guige', guige)
                        print('company', company)

                        with open('yao.csv', 'a', encoding='utf-8') as f:
                            f.write(f'{name}, {p_text}, {guige}, {company}\n')


if __name__ == '__main__':
    main()
