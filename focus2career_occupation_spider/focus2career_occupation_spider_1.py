# -*- coding: utf-8 -*-
"""Focus 2 Career 职业信息采集脚本。

从职业信息页面解析职业概述、任务、兴趣、技能、价值观、工作环境、教育要求和专业协会等字段。
历史登录会话信息和采集结果示例已删除。
"""
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


def parse_detail_data(res, leibie, zhiyemingcheng, all_data_list):
    data = {
        'fenlei': leibie,
        'zhiyemingcheng': zhiyemingcheng,
        'occupation_overview': '',
        'job_tasks': '',
        'work_interest_profile': '',
        'skills': '',
        'values': '',
        'work_conditions': '',
        'education_requirements1': '',
        'education_requirements2': '',
        'advancement': '',
        'professional_association': '',
    }
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

            # Occupation Overview
            if 'Occupation Overview' in h2:
                p_list = div.xpath('./div//p//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                data['occupation_overview'] = p_text
                continue

            # Job Tasks
            if 'Job Tasks' in h2:
                p_list = div.xpath('./div//p//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['job_tasks'] = p_text
                continue

            # Work Interest Profile
            if 'Work Interest Profile' in h2:
                p_list = div.xpath('./div//p//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['work_interest_profile'] = p_text
                continue

            # Skills
            if 'Skills' in h2:
                p_list = div.xpath('./div/div//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['skills'] = p_text
                continue

            # Values
            if 'Values' in h2:
                p_list = div.xpath('./div/div//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['values'] = p_text
                continue

            # Work Conditions
            if 'Work Conditions' in h2:
                p_list = div.xpath('./div/div//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['work_conditions'] = p_text
                continue

            # Education Requirements
            if 'Education Requirements' in h2:
                p_list = div.xpath('./div/div//text()')
                # print(p_list)
                p_text = ''
                # Education Requirements前部分
                for p in p_list[:8]:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['education_requirements1'] = p_text

                p_text = ''
                # Education Requirements后部分
                for p in p_list[8:]:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['education_requirements2'] = p_text
                continue

            # Advancement
            if 'Advancement' in h2:
                p_list = div.xpath('./div/div//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['advancement'] = p_text
                continue

            # Professional Association
            if 'Professional Association' in h2:
                p_list = div.xpath('./div/div//text()')
                p_text = ''
                for p in p_list:
                    if p.strip():
                        p_text += p.strip() + '\n'
                # print(p_text)
                data['professional_association'] = p_text
                continue

    all_data_list.append(data)
    print(data)
    return all_data_list


def save_data(all_data_list):
    # 新建excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '分类'
    sheet['B1'] = '职业名称'
    sheet['C1'] = '职业概述'
    sheet['D1'] = '工作任务'
    sheet['E1'] = '工作兴趣简介'
    sheet['F1'] = '技能'
    sheet['G1'] = '价值观'
    sheet['H1'] = '工作环境'
    sheet['I1'] = '教育要求'
    sheet['J1'] = '相关专业'
    sheet['K1'] = '进步'
    sheet['L1'] = '专业协会'
    i = 2

    for data in all_data_list:
        sheet[f'A{i}'] = data['fenlei']
        sheet[f'B{i}'] = data['zhiyemingcheng']
        sheet[f'C{i}'] = data['occupation_overview']
        sheet[f'D{i}'] = data['job_tasks']
        sheet[f'E{i}'] = data['work_interest_profile']
        sheet[f'F{i}'] = data['skills']
        sheet[f'G{i}'] = data['values']
        sheet[f'H{i}'] = data['work_conditions']
        sheet[f'I{i}'] = data['education_requirements1']
        sheet[f'J{i}'] = data['education_requirements2']
        sheet[f'K{i}'] = data['advancement']
        sheet[f'L{i}'] = data['professional_association']
        i += 1
    wb.save('focus2career.xlsx')


def main():
    # 第一页url
    first_url = 'https://www.focus2career.com/LoggedIn/OccupationSearchByIndustry.cfm?Unique={ts%20%272022-10-12%2018:41:21%27}'
    # 1. 第一页请求
    first_res = get_data(first_url)

    # 2. 解析第一页数据
    div_list = parse_first_data(first_res)
    # 保存所有数据的列表
    all_data_list = []
    num = 1
    for div in div_list:
        # 获取类别名,职业名称,职业href
        leibie = div.xpath('./div/h2/text()')[0].strip()
        a_list = div.xpath('./div/div/table/tbody/tr/th/a')
        for a in a_list:
            print(f'开始获取第{num}个...')
            zhiye_name = a.xpath('./text()')[0]
            href = a.xpath('./@href')
            href = urljoin(first_url, href[0])

            # 3. 逐个发送请求,获取响应数据
            detail_res = get_data(href)
            # 4. 解析数据
            parse_detail_data(detail_res, leibie, zhiye_name, all_data_list)

            num += 1
    save_data(all_data_list)


if __name__ == '__main__':
    main()
