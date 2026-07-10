# -*- coding: utf-8 -*-
"""国家标准信息公共服务平台 SAMR 国家标准采集脚本。

按关键词分页检索国家标准，进入详情页提取标准号、名称、类别、批准日期和实施日期，并写入 Excel。
"""
# @Time: 2022/9/26 17:48
import requests
import random
from lxml import etree
import time
import openpyxl


user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    ]


def get_data(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    res = requests.get(url, headers=headers)
    time.sleep(random.choice([2, 3, 4]))

    return res


def parse_and_save_data():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '#'
    sheet['B1'] = '标准号'
    sheet['C1'] = '标准名称'
    sheet['D1'] = '行业领域'
    sheet['E1'] = '标准类别'
    sheet['F1'] = '状态'
    sheet['G1'] = '批准日期'
    sheet['H1'] = '实施日期'
    sheet['I1'] = '备案号'
    sheet['J1'] = '备案日期'

    i = 2
    for page in range(1, 25):
        print(f'开始获取第{page}页...')
        url = f'https://std.samr.gov.cn/search/stdPage?tid=&q=%E6%99%BA%E8%83%BD&op=G_STD_DOMAIN%3A%22%E5%9B%BD%E5%AE%B6%E6%A0%87%E5%87%86%22&pageNo={page}'
        res = get_data(url)
        print(f'第{page}页获取成功!!!')
        # with open('zhineng.html', 'w', encoding='utf-8') as f:
        #     f.write(res.text)
        # print(res.text)

        tree = etree.HTML(res.text)
        pid_list = tree.xpath('//a/@pid')

        for pid in pid_list:
            href = 'https://std.samr.gov.cn/gb/search/gbDetailed?id=' + pid
            detail_res = get_data(href)
            # with open('detail.html', 'w', encoding='utf-8') as f:
            #     f.write(detail_res.text)
            # print(detail_res.text)

            # 行业领域		状态			备案号	备案日期
            detail_tree = etree.HTML(detail_res.text)
            # 标准名称
            name = detail_tree.xpath('//div[@class="page-header"]/h4/text()')[0]

            dls = detail_tree.xpath('//div[@class="container main-body"]/div/div/div/div[6]/dl')
            # 标准号
            num = dls[0].xpath('./dd[1]/text()')[0]
            # 批准日期
            public_date = dls[0].xpath('./dd[2]/text()')[0]
            # 实施日期
            date = dls[0].xpath('./dd[3]/text()')[0].strip().replace('\n', '').replace('\r', '')

            # 标准类别
            category = dls[1].xpath('.//dd[1]/text()')[0]

            print(num, name, category, public_date, date)

            sheet[f'B{i}'] = num
            sheet[f'C{i}'] = name
            sheet[f'E{i}'] = category
            sheet[f'G{i}'] = public_date
            sheet[f'H{i}'] = date
            i += 1

    wb.save('samr.xlsx')


def main():
    parse_and_save_data()


if __name__ == '__main__':
    main()
