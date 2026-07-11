# -*- coding = utf-8 -*-
"""Wikipedia 印度尼西亚行政区与人口信息采集脚本。"""
# @Time: 2022/10/6 11:02
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
        # 'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
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


def parse_first_data(first_res):
    # 使用xpath获取,每个地区
    tree = etree.HTML(first_res.text)
    # tables = tree.xpath('//div[@class="mw-parser-output"]/table')
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
    # wb = openpyxl.Workbook()
    # sheet = wb.active
    # sheet['A1'] = '县/市'
    # sheet['B1'] = '人口数量'
    # i = 2
    wb = openpyxl.load_workbook('人口数量.xlsx')
    sheet = wb.active
    i = 6307
    # 发送请求,获取第一页数据
    first_url = 'https://en.wikipedia.org/wiki/List_of_regencies_and_cities_of_Indonesia'
    first_res = get_data(first_url)
    # 解析数据
    hrefs = parse_first_data(first_res)
    # 获取514个县或市链接
    hrefs = hrefs[400: -19]
    # hrefs = hrefs[300: 400]
    all_num = len(hrefs)

    for num, href in enumerate(hrefs):
        href = urljoin(first_url, href)
        print(f'开始访问第{num+1}个县或市,共有{all_num}个...')
        # href = 'https://en.wikipedia.org/wiki/Yahukimo_Regency'
        res = get_data(href)
        tree = etree.HTML(res.text)
        tables = tree.xpath('//table')
        for table in tables:
            index = i
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
                        i += 1
                        for tr in trs[1:-1]:
                            # th_num_up = 1
                            if th_num_up == 1:
                                name = tr.xpath(f'./td[1]//text()')
                            elif th_num_up == 2:
                                name = tr.xpath(f'./td[2]//text()')
                            people = tr.xpath(f'./td[{th_index+1}]//text()')
                            if name:
                                name = name[0]
                            if people:
                                people = people[0].replace(',', '')
                            print(name, people)

                            name = name.replace('\n', '').replace(' ', '')
                            people = people.replace('\n', '').replace('\r', '').replace(' ', '')
                            print(i, name, people)

                            sheet[f'A{i}'] = name
                            sheet[f'B{i}'] = people
                            i += 1
                            # print(index, name, people)

                        people = trs[-1].xpath(f'./td[{th_index + 1}]//text()')
                        if not people:
                            people = trs[-1].xpath(f'./th[{th_index + 1}]//text()')
                        people = people[0].replace('\n', '').replace('\r', '').replace(' ', '').replace(',', '')

                        name = 'totals for ' + href.split('/')[-1]
                        sheet[f'A{index}'] = name
                        sheet[f'B{index}'] = people
                        i += 1
                        print(index, name, people)
                        break
            except Exception as e:
                print(e)
                print(f'{href}存储数据失败...')
                with open('shibai.txt', 'a', encoding='utf-8') as f:
                    f.write(href + '\n')

    # 保存文件
    wb.save('人口数量.xlsx')


if __name__ == '__main__':
    main()
