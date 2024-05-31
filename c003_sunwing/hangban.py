# -*- coding = utf-8 -*-
# @Time: 2022/9/11 09:52
"""
获取航班信息
"""
import requests
from lxml import etree
import json
import openpyxl


# 获取国家的二位字母代码
def get_country_code(key):
    url = f'https://jichang.gjcha.com/so/{key}__jichang/'
    res = requests.get(url)
    tree = etree.HTML(res.text)
    tr_list = tree.xpath('//*[@class="table table-bordered"]/tbody/tr')
    # print(tr_list)
    for tr in tr_list:
        if key == tr.xpath('./td[2]/text()')[0]:
            area = tr.xpath('./td[5]/a/text()')[0].split(' ')[0]

    with open('area_code.json', 'r', encoding='utf-8') as f:
        dic_json = f.read()

    dic = json.loads(dic_json)
    if area == '圣马丁(荷属)':
        area = '荷属圣马丁'
    return dic[area]


def get_data(url):
    # 发送请求,获取响应
    res = requests.get(url)

    return res


# 存放航班信息的表格
def new_excel():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '出发城市'
    sheet['B1'] = '到达城市'
    sheet['C1'] = '出发国家'
    sheet['D1'] = '到达国家'
    sheet['E1'] = '国内/国际'

    return wb, sheet


def main():
    i = 2
    # 1. 创建excel,存放航班信息
    wb, sheet = new_excel()
    # 2. 发送请求,获取所有城市
    all_url = 'https://services.sunwinggroup.ca/beta/api/search/getGatewayforBrand/en/SWG/RE'
    res = get_data(all_url)
    for country_name in res.json():
        code = country_name['code']
        departure_country_code = get_country_code(code)

        # 3. 发送请求,获取一个城市的航班
        url = f'https://services.sunwinggroup.ca/beta/api/search/getDestCode/en/SWG/{code}/RE'
        res = get_data(url)
        airports = res.json()
        for airport in airports:
            destination_code = airport['destinationCode']
            destination_country_code = get_country_code(destination_code)

            if departure_country_code == destination_country_code:
                mode = 'DOM'
            else:
                mode = 'INT'
            sheet[f'A{i}'] = code
            sheet[f'B{i}'] = destination_code
            sheet[f'C{i}'] = departure_country_code
            sheet[f'D{i}'] = destination_country_code
            sheet[f'E{i}'] = mode
            print(f'出发城市: {code},出发国家: {destination_code},到达城市: {departure_country_code},到达国家: {destination_country_code}')
            i += 1

    wb.save('hangbang.xlsx')


if __name__ == '__main__':
    main()
