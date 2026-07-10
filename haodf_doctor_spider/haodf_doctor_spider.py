# -*- coding: utf-8 -*-
"""好大夫在线妇产科医生公开信息采集脚本。

按地区分页采集医生姓名、性别、职称、医院名称、公开联系电话、地址和门诊时间。
仅用于公开信息采集学习，请遵守网站规则和个人信息保护要求。
"""
# @Time: 2022/12/1 18:37
import requests
import time
import random
from lxml import etree
import re


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    for i in range(10):
        try:
            res = requests.get(url, headers=headers, timeout=10)
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
    # 获取所有链接
    li_list = tree.xpath('//div[@class="d-doc-list"]/ul/li')
    return li_list


def save_data(li_list):
    # 循环取出每个人的信息
    for li in li_list:
        # 姓名
        name = li.xpath('./div/div/p[1]/span[1]/a/text()')
        if name:
            name = name[0].strip()
        # print(1, name)

        # 职称
        title = li.xpath('./div/div/p[1]/span[2]//text()')
        if title:
            title = title[0].strip().replace(' ', '')
        # print(2, title)

        # 医院名称
        hospital = li.xpath('./div/div/p[2]/text()')
        if hospital:
            hospital = hospital[0].strip().replace(' ', '')
        # print(3, hospital)

        # 获取医生页面,获取详细信息
        href = li.xpath('./div/div/p[1]/span[1]/a/@href')
        # print(10, href)
        if href:
            href = href[0]
        dor_res = get_data(href)

        # 性别
        # 使用正则匹配简介信息
        pattern = r'headline(.*?)。"'
        result = re.findall(pattern, dor_res.text)
        if result:
            result = result[0]
        if '男' in result:
            gender = '男'
        elif '女' in result:
            gender = '女'
        else:
            gender = '-'
        # print(4, gender)

        # 电话(手机)
        # 拼接获取电话的url
        new_url = href[:-5] + '/xinxi-menzhen.html'
        tel_res = get_data(new_url)
        # print(tel_res.text)

        # 使用正则获取电话
        pattern = r'content-num(.*?)span'
        result = re.findall(pattern, tel_res.text)
        # print(11, result)
        all_tel = []
        for tel in result:
            tel = re.search(r'\d+-\d+', tel).group()
            # print(12, tel)
            all_tel.append(tel)
        tel = ' '.join(all_tel)

        # 地址
        # 使用正则匹配
        pattern = r'hospitalAddress":"(.*?)"'
        result = re.findall(pattern, tel_res.text)
        address = '、'.join(list(set(result)))
        # print(14, address)

        # 门诊时间
        pattern = r'description" content="(.*?)"'
        result = re.findall(pattern, tel_res.text)
        description = result[0].split('：')[-1]

        with open('hospital.csv', 'a', encoding='utf-8') as f:
            f.write(f'{name},{gender},{title},{tel},{hospital},{address},{description}\n')

        print(f'{name},{gender},{title},{tel},{hospital},{address},{description}')


def main():
    with open('hospital.csv', 'w', encoding='utf-8') as f:
        f.write('姓名,性别,职称,电话,医院名称,地址,门诊时间\n')
    # 上海和湖北
    city_dic = {
        'shanghai': 'https://www.haodf.com/doctor/list-31-fuchankezonghe.html?p={page}',
        'hubei': 'https://www.haodf.com/doctor/list-42-fuchankezonghe.html?p={page}'
    }
    # 页码
    page_dic = {
        'shanghai': 80,
        'hubei': 153
    }

    # 1.发送请求,获取数据
    for city_key, city_url in city_dic.items():
        for page in range(1, page_dic[city_key] + 1):
            res = get_data(city_url.format(page=page))

            # 2. 解析数据
            li_list = parse_data(res)

            # 3.向每一个链接发送请求
            save_data(li_list)


if __name__ == '__main__':
    main()
