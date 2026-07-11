# -*- coding = utf-8 -*-
"""Wikipedia 印度尼西亚行政区与人口信息采集脚本。"""
# @Time: 2022/10/10 10:54
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
    h4_list = tree.xpath('//div[@class="mw-parser-output"]/h4')
    table_list = tree.xpath('//div[@class="mw-parser-output"]/table')
    # hrefs = tree.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr/td[2]/a/@href')
    return h4_list, table_list


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
    sheet['A1'] = '省名称'
    sheet['B1'] = '市/县名称'
    sheet['C1'] = '镇名称'
    sheet['D1'] = '人口数量'
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
    h4_list, table_list = parse_first_data(first_res)
    shi_i = 0
    for num, h4 in enumerate(h4_list[:37]):
        sheng = h4.xpath('./span/text()')
        shi_list = table_list[num+1].xpath('./tbody/tr/td[2]/a/text()')
        shi_href_list = table_list[num+1].xpath('./tbody/tr/td[2]/a/@href')
        for shi_num, shi in enumerate(shi_list):
            shi_href = shi_href_list[shi_num]
            shi_href = urljoin(first_url, shi_href)
            shi_i += 1
            print(f'正在获取{sheng[0]}省,{shi}市,第{shi_i}个市,共有514个市...')

            res = get_data(shi_href)

            if not res:
                wb.save('市区人口数量.xlsx')
                print('访问错误,终止程序!!!')
                sys.exit()

            tree = etree.HTML(res.text)
            tables = tree.xpath('//table')
            for table in tables:
                ths = table.xpath('./tbody/tr/th')
                try:
                    for th_num_up, th_up in enumerate(ths):
                        th_text = ''.join(th_up.xpath('.//text()'))
                        if (th_num_up == 1 and 'Area' in th_text) or (th_num_up == 2 and 'Area' in th_text):
                            th_index = None

                            for th_num, th in enumerate(ths):
                                th_text = ' '.join(th.xpath('.//text()'))
                                if '2022' in th_text:
                                    # print(th_num, th_text)
                                    th_index = th_num
                                    print('2022', th_index)
                                    break
                                if '2021' in th_text:
                                    # print(th_num, th_text)
                                    th_index = th_num
                                    print('2021', th_index)
                                    break
                                elif '2020' in th_text:
                                    # print(th_num, th_text)
                                    th_index = th_num
                                    print('2020', th_index)
                                elif '2010' in th_text:
                                    # print(th_num, th_text)
                                    th_index = th_num
                                    print('2010', th_index)
                            if not th_index:
                                break
                            trs = table.xpath('./tbody/tr')
                            print(th_index)

                            for tr in trs[1:]:
                                # th_num_up = 1
                                if th_num_up == 1:
                                    name = tr.xpath(f'./td[1]//text()')
                                elif th_num_up == 2:
                                    name = tr.xpath(f'./td[2]//text()')
                                people = tr.xpath(f'./td[{th_index + 1}]//text()')
                                if name:
                                    name = name[0].replace('\n', '')
                                    if 'otal' in name:
                                        continue
                                if people:
                                    people = people[0].replace(',', '')

                                name = name.replace('\n', '').replace(' ', '')
                                people = people.replace('\n', '').replace('\r', '').replace(' ', '')

                                sheet[f'A{i}'] = sheng[0]
                                sheet[f'B{i}'] = shi
                                sheet[f'c{i}'] = name
                                sheet[f'd{i}'] = people

                                print(i, sheng[0], shi, name, people)
                                i += 1
                except Exception as e:
                    print(e)
                    print(f'{shi_href}存储数据失败...')
                    # with open('shibai.txt', 'a', encoding='utf-8') as f:
                    #     f.write(shi_href + '\n')
        # break

    wb.save('印尼人口数量.xlsx')


if __name__ == '__main__':
    main()
