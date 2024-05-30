# -*- coding = utf-8 -*-
# @Time: 2024/5/27 21:41
# @Author: ZhouYanHui
import os
import pandas as pd
import requests
from lxml import etree
import time
import random
import re
import csv


user_agent = [
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
    'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.1; AOLBuild 4334.5012; Windows NT 6.0; WOW64; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
    'Mozilla/5.0 (X11; U; Linux; ru-RU) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: 802 025a17d)',
    'Mozilla/5.0 (X11; U; Linux; pt-PT) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4'
    'Mozilla/5.0 (X11; U; Linux; en-GB) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 239 52c6958)',
]


def get_data(url):
    print('正在请求:', url)
    # 获取数据
    headers = {
        'User-Agent': random.choice(user_agent),
    }

    for _ in range(5):
        try:
            res = requests.get(
                url,
                headers=headers,
                timeout=10,
                # proxies=proxies
            )
        except:
            continue
        res.encoding = 'utf-8'
        time.sleep(random.randint(2, 4))
        if res.status_code == 200 and res:
            return res


def parse_lusha(res):
    # 解析网页数据
    tree = etree.HTML(res.text)
    a_list = tree.xpath('/html/body/main/div[1]/section[1]/div/div/div/div/div/a')
    return a_list


def pares_linkedin_url(detail_res):
    # 解析linkedin网址
    tree = etree.HTML(detail_res.text)
    linkedin_url = tree.xpath('//*[@class="company-details-socials p-0 m-0"]/li/a/@href')
    return linkedin_url


def parse_linkedin(linkedin_res):
    # 使用re获取website
    p = re.compile(r'"sameAs":"(.*?)"}')
    result = p.findall(linkedin_res.text)
    if result:
        website = result[0]
    else:
        website = ''

    linkedin_tree = etree.HTML(linkedin_res.text)
    text = linkedin_tree.xpath('//*[@class="break-words whitespace-pre-wrap text-color-text"]/text()')
    if text:
        text = text[0].strip().replace(',', '.')
    else:
        text = ''

    return website, text


def lusha(title_list, data_list):
    # 获取lusha网站上的数据信息
    # for page in range(1, 26+1):
    for page in range(1, 26+1):
        # https://www.lusha.com/company-search/environmental-services/31/australia/217/
        # https://www.lusha.com/company-search/environmental-services/31/australia/217/page/2/
        url = f'https://www.lusha.com/company-search/environmental-services/31/australia/217/page/{page}/'

        # 发送请求,获取数据
        res = get_data(url)
        # 解析网站数据
        a_list = parse_lusha(res)
        # 使用selenium获取数据
        # selenium_get_data(a_list)
        for a in a_list:
            href = a.xpath('./@href')
            name = a.xpath('./text()')[0].strip()

            if name in title_list:
                continue

            print(name)
            if href:
                href = href[0]

                # 发送请求获取linkedin_url
                detail_res = get_data(href)
                # print(detail_res)
                linkedin_url = pares_linkedin_url(detail_res)

                if linkedin_url:
                    linkedin_url = linkedin_url[0]

                    # 发送请求获取LinkedIn页面数据
                    # selenium_get_data(linkedin_url)
                    linkedin_res = get_data(linkedin_url)
                    # print(linkedin_res.text)

                    # 解析数据
                    if linkedin_res:
                        website, text = parse_linkedin(linkedin_res)
                    else:
                        website, text = '', ''

                    print(name, linkedin_url, website, text)

                    data_list.append([name, linkedin_url, website, text])


def main():
    # 判断csv文件是否存在
    if os.path.exists('lusha.csv'):
        df = pd.read_csv('lusha.csv')
        title_list = df['Title'].to_list()
    else:
        title_list = []

    # 保存获取的数据
    data_list = []

    try:
        lusha(title_list, data_list)
    except Exception as e:
        print(e)

    # 保存数据到csv
    if os.path.exists('lusha.csv'):
        with open('lusha.csv', 'a') as f:
            write = csv.writer(f)
            for data in data_list:
                write.writerow(data)
    else:
        with open('lusha.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(['Title', 'Website', 'LinkedIn URL', 'Description'])
            for data in data_list:
                write.writerow(data)


if __name__ == '__main__':
    main()
