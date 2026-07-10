# -*- coding: utf-8 -*-
"""Focus 2 Career 职业信息采集脚本。

从职业信息页面解析职业概述、任务、兴趣、技能、价值观、工作环境、教育要求和专业协会等字段。
历史登录会话信息和采集结果示例已删除。
"""
# @Time: 2022/10/14 16:50
# -*- coding: utf-8 -*-
# @Time: 2022/10/13 11:06
import requests
from lxml import etree
from urllib.parse import urljoin
import openpyxl
import random
import time


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    for i in range(10):
        try:
            res = requests.get(url, headers=headers)
            # time.sleep(random.choice([2, 3, 4]))
            print(f'请求成功:{url}')
            if res and res.status_code == 200:
                return res
        except Exception as e:
            print(url)
            print('出错了,正在重试...', e)
            if i == 9:
                with open('shibai.txt', 'a', encoding='utf-8') as f:
                    f.write(url + '\n')


def parse_first_data(res):
    # 使用xpath获取数据
    tree = etree.HTML(res.text)
    div_list = tree.xpath('//*[@id="accordion"]/div/div')

    return div_list


def parse_detail_data(res, values_list, skills_list, num):
    # 使用xpath获取数据
    tree = etree.HTML(res.text)
    div_list = tree.xpath('//*[@id="accordion"]/div/div')

    # 循环div获取数据
    for div in div_list:
        h2 = div.xpath('./div/h2/text()')
        if h2:
            if len(h2) > 1:
                h2 = h2[1].strip()
            else:
                h2 = h2[0].strip()

            # Skills
            if 'Skills' in h2:
                h3_list = div.xpath('./div/div/h3')
                for i in range(1, len(h3_list)+1):
                    h3_text = div.xpath(f'./div/div/h3[{i}]//text()')[0].strip()
                    p_text = div.xpath(f'./div/div/p[{i}]//text()')[0].strip()
                    dic = dict()
                    dic['name'] = h3_text
                    dic['content'] = p_text
                    dic['num'] = num + 1
                    skills_list.append(dic)
                # print(skills_list)
                continue

            # Values
            if 'Values' in h2:
                h3_list = div.xpath('./div/div/h3')
                for i in range(1, len(h3_list) + 1):
                    h3_text = div.xpath(f'./div/div/h3[{i}]//text()')[0].strip()
                    p_text = div.xpath(f'./div/div/p[{i}]//text()')[0].strip()
                    dic = dict()
                    dic['name'] = h3_text
                    dic['content'] = p_text
                    dic['num'] = num + 1
                    values_list.append(dic)
                # print(values_list)
                continue


def save_data(skills_list, values_list):
    # 新建excel
    # value
    wb_value = openpyxl.Workbook()
    sheet_value = wb_value.active
    sheet_value['A1'] = '主键'
    sheet_value['B1'] = '名称'
    sheet_value['C1'] = '内容'
    i_value = 2

    # skills
    wb_skills = openpyxl.Workbook()
    sheet_skills = wb_skills.active
    sheet_skills['A1'] = '主键'
    sheet_skills['B1'] = '名称'
    sheet_skills['C1'] = '内容'
    i_skills = 2

    for data in values_list:
        sheet_value[f'A{i_value}'] = data['num']
        sheet_value[f'B{i_value}'] = data['name']
        sheet_value[f'C{i_value}'] = data['content']
        i_value += 1
    wb_value.save('values.xlsx')

    for data in skills_list:
        sheet_skills[f'A{i_skills}'] = data['num']
        sheet_skills[f'B{i_skills}'] = data['name']
        sheet_skills[f'C{i_skills}'] = data['content']
        i_skills += 1
    wb_skills.save('skills.xlsx')


def main():
    # 第一页url
    first_url = 'https://www.focus2career.com/LoggedIn/OccupationSearchByIndustry.cfm?Unique={ts%20%272022-10-12%2018:41:21%27}'
    # 1. 第一页请求
    first_res = get_data(first_url)

    # 2. 解析第一页数据
    div_list = parse_first_data(first_res)
    # 保存数据的列表
    values_list = []
    skills_list = []
    num = 1
    for div in div_list:
        # 获取类别名,职业名称,职业href
        a_list = div.xpath('./div/div/table/tbody/tr/th/a')
        for a in a_list:
            print(f'开始获取第{num}个...')
            href = a.xpath('./@href')
            href = urljoin(first_url, href[0])

            # 3. 逐个发送请求,获取响应数据
            detail_res = get_data(href)
            # 4. 解析数据
            parse_detail_data(detail_res, values_list, skills_list, num)
            num += 1
        #     break
        # break
    save_data(skills_list, values_list)


if __name__ == '__main__':
    main()
