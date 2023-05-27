# -*- coding = utf-8 -*-
# @Time: 2022/9/7 15:19
import time
import requests
from lxml import etree


def get_data(headers):
    url = 'https://www.tianyancha.com/search'
    params = {
        'key': '北方华创科技集团股份有限公司'
        # 'key': '北方'
    }

    # 发送请求,获取响应
    res = requests.get(url, params=params, headers=headers)

    return res


def parse_data(res):
    html_data = etree.HTML(res.text)
    # 使用xpath获取href
    href = html_data.xpath(
        '//*[@id="page-container"]/div/div[2]/section/main/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/a/@href'
    )[0]

    return href


def get_company_data(headers, href):
    url = 'https://capi.tianyancha.com/cloud-listed-company/listed/aShareBaseInfo.json'
    params = {
        '_': int(time.time() * 1000),
        'gid': href.split('/')[-1]
    }

    # 发送请求,获取响应
    res = requests.get(url, params=params, headers=headers)
    data_dic = res.json()

    # 公司名称
    company_name = data_dic['data']['companyName']
    # 主营业务
    main_business = data_dic['data']['mainBusiness']
    # 所属行业
    industry = data_dic['data']['industry']
    # A股代码
    code = data_dic['data']['code']
    # A股简称
    name = data_dic['data']['name']

    print(f'公司名称: {company_name}')
    print(f'主营业务: {main_business}')
    print(f'所属行业: {industry}')
    print(f'A股代码: {code}')
    print(f'A股简称: {name}')


def main():
    # headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 1. 发送请求,获取公司网站数据
    res = get_data(headers)
    # 2. 解析数据,获取网站
    href = parse_data(res)
    # 3. 请求公司网页
    get_company_data(headers, href)


if __name__ == '__main__':
    main()
