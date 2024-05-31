# -*- coding = utf-8 -*-
# @Time: 2022/9/11 17:08
import requests
import re
import json
from lxml import etree


# def get_data():
#     url = 'https://www.sunwing.ca/page-data/en/promotion/flights/cheap-flights/from-calgary/page-data.json'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
#     }
#     res = requests.get(url, headers=headers)
#     # print(res.text)
#     # print('-'*100)
#     pattern = r'Flights","Offers":(.*)}]},{"Gateway":{"Code":"YEG",'
#     info_str = re.findall(pattern, res.text)[0]
#     info_json = json.loads(info_str)
#     for info in info_json:
#         print(info)
#
#     # print(info_json)
#     # print(type(info_json))


def get_data(url, params=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    res = requests.get(url, headers=headers, params=params)
    # print(res.text)
    return res


def main():
    # 1. 发送请求,获取航班详情页网址
    print('获取所有航班网址...')
    all_url = 'https://www.sunwing.ca/page-data/en/promotion/flights/cheap-flights/from-winnipeg/page-data.json'
    res = get_data(all_url)

    # 使用正则匹配每个航班的信息
    pattern = r'DeepLink":"(.*?)","DepartureDate'
    # comp = re.compile(pattern)
    info_str = re.findall(pattern, res.text)

    # 2. 发送请求,获取每个航班信息
    for info in info_str:
        info_url = 'https:' + info
        print('发送请求获取sid:', info_url)
        info_res = get_data(info_url)

        # 获取sid
        pattern = r'"sid" value="(.*?)">'
        sid = re.findall(pattern, info_res.text)[0]
        print('sid:', sid)

        info_url_sid = info_url + '&sid=' + sid
        info_url_sid = info_url_sid.replace('handler', 'results')

        print('发送请求,获取航班信息:', info_url_sid)

        info_res_sid = get_data(info_url_sid)

        # 3. 解析数据,获取航班数据
        tree = etree.HTML(info_res_sid.text)

        tr_list = tree.xpath('//*[@id="content"]/div[2]/section/form/div/div/table/tr')
        for tr in tr_list:
            # 航班号
            airline = tr.xpath('./td[1]/div/a/text()')[0]

            # 出发时间
            week = tr.xpath('./td[2]/table/tbody/tr/td[1]/div/span[1]//text()')[0]
            month_day = tr.xpath('./td[2]/table/tbody/tr/td[1]/div/span[2]//text()')[0]
            year = tr.xpath('./td[2]/table/tbody/tr/td[1]/div/span[3]/text()')[0]
            hour = tr.xpath('./td[2]/table/tbody/tr/td[2]/text()')[-1].split('\\')[0].strip('\n                                                    ')
            deper_date = year + ' ' + month_day + ' ' + week +' ' + hour

            # 到达时间
            dest_date = tr.xpath('./td[2]/table/tbody/tr/td[3]/text()')
            dest_date = ' '.join(dest_date).strip('\n                                                    ')

            # 持续时间
            duration = tr.xpath('./td[3]/text()')[0]

            # 票价
            td_list = tr.xpath('./td[6]/table/tbody/tr/td')
            price_list = []
            for td in td_list:
                price = td.xpath('./div/label/span/text()')[0]
                price_list.append(price)

            print(f'航班号:{airline}, 出发时间{deper_date}, 到达时间{dest_date}, 飞行时长{duration}, 价格{price_list}')


if __name__ == '__main__':
    main()
