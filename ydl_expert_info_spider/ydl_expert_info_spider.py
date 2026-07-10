# -*- coding: utf-8 -*-
# @Time: 2022/9/23 20:55
"""ydl.com 专家信息采集脚本。

历史登录凭据和访问会话信息已删除，只保留采集字段、页面解析和 Excel 写入逻辑。
如需重新运行，请根据当前网站结构和合法访问方式调整请求参数。
"""
import requests
from lxml import etree
from urllib.parse import urljoin
import openpyxl
import time
import random


def get_data(url, extra_headers=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    if extra_headers:
        headers.update(extra_headers)
    res = requests.get(url, verify=False, headers=headers)
    # print(res.text)
    # time.sleep(random.choice([1, 2, 3]))
    return res


def parse_and_save_data():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '专家姓名'
    sheet['B1'] = '性别'
    sheet['C1'] = '咨询数'
    sheet['D1'] = '在线帮助人数'
    sheet['E1'] = '总时长'
    sheet['F1'] = '起价'
    sheet['G1'] = '好评率'
    sheet['H1'] = '评价条数'
    sheet['I1'] = '评价星级'
    sheet['J1'] = '从业年限'
    # sheet['K1'] = '教育背景'
    # sheet['L1'] = '专业资质'

    j = 2

    # 历史访问会话信息已删除，保留男女分类循环结构。
    # 如果当前页面需要筛选参数，请按网站现有公开参数重新配置。
    gender_headers = {
        'male': {},
        'female': {},
    }
    phone_url = 'https://m.ydl.com/jy/experts'
    for i in range(25):
        print(f'开始爬取女专家第{i + 1}页...')
        url = f'https://www.ydl.com/experts/p{i + 1}'
        res = get_data(url, gender_headers['female'])
        print(f'女专家第{i + 1}页请求完成!')
        tree = etree.HTML(res.text)
        div_list = tree.xpath('//div[@class="expertsList_items"]/div')
        for div in div_list:
            href = div.xpath('./div/h3/a/@href')
            if href:
                href_phone = urljoin(phone_url, href[0])
                href_pc = urljoin(url, href[0])
                # 'https://m.ydl.com/jy/experts/1739'
                # 'https://www.ydl.com/experts/18935'
                name = div.xpath('./div/h3/a/text()')[0].strip()
                print(f'开始获取{name}的主页面...')
                print(href_phone)
                print(href_pc)
                res_phone = get_data(href_phone)
                res_pc = get_data(href_pc)
                # print(res_phone.text)
                print(f'{name}的主页面获取完成!')
                # print(res.text)
                tree_phone = etree.HTML(res_phone.text)
                tree_pc = etree.HTML(res_pc.text)
                zixun = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[3]/dd/text()')[0].strip()
                print(zixun)
                zaixian  = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[2]/dd/text()')[0].strip()
                print(zaixian)
                shichang = tree_phone.xpath('//*[@id="app"]/div/div/div/div[2]/div[3]/div/div/p[2]/i/text()')[0].strip()
                print(shichang)
                qijia = tree_pc.xpath('/html/body/div[6]/div[3]/div/div[2]/div/div[2]/p[1]/span/text()')[0].strip()
                print(qijia)
                haoping = tree_pc.xpath('/html/body/div[6]/div[1]/div/div/div/span[2]/text()')
                if haoping:
                    haoping = haoping[0].strip()
                else:
                    haoping = ''
                print(haoping)
                pingjiashu = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[4]/dd/text()')[0].strip()
                print(pingjiashu)
                pingjiaxingji = tree_pc.xpath('/html/body/div[6]/div[1]/div/div/div/span[1]/text()')[0].strip()
                print(pingjiaxingji)
                congyenianxian = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[1]/dd/text()')[0].strip()
                print(congyenianxian)
                # jiaoyubeijing = tree_phone.xpath('//div[@class="line_con_edu"]/p//text()')[0].strip()
                # print(jiaoyubeijing)
                # zhuanyezizhi = tree_phone.xpath('//p[@class="line_con_pro"]//text()')[0].strip()
                # print(zhuanyezizhi)

                # 专家姓名、性别、咨询数、在线帮助人数、总时长、起价、好评率、评价条数、评价星级、从业年限、教育背景、专业资质
                sheet[f'A{j}'] = name
                sheet[f'B{j}'] = '女'
                sheet[f'C{j}'] = zixun
                sheet[f'D{j}'] = zaixian
                sheet[f'E{j}'] = shichang
                sheet[f'F{j}'] = qijia
                sheet[f'G{j}'] = haoping
                sheet[f'H{j}'] = pingjiashu
                sheet[f'I{j}'] = pingjiaxingji
                sheet[f'J{j}'] = congyenianxian
                # sheet[f'K{j}'] = pingjia
                # sheet[f'L{j}'] = pingjia
                print(f'{name}下载完毕!')

                j += 1

    for i in range(9):
        print(f'开始爬取男专家第{i + 1}页')
        url = f'https://www.ydl.com/experts/p{i + 1}'
        res = get_data(url, gender_headers['male'])
        print(f'男专家第{i + 1}页请求完成!')
        tree = etree.HTML(res.text)
        div_list = tree.xpath('//div[@class="expertsList_items"]/div')
        for div in div_list:
            href = div.xpath('./div/h3/a/@href')
            if href:
                href_phone = urljoin(phone_url, href[0])
                href_pc = urljoin(url, href[0])
                # 'https://m.ydl.com/jy/experts/1739'
                # 'https://www.ydl.com/experts/18935'
                name = div.xpath('./div/h3/a/text()')[0].strip()
                print(f'开始获取{name}的主页面...')
                print(href_phone)
                print(href_pc)
                res_phone = get_data(href_phone)
                res_pc = get_data(href_pc)
                # print(res_phone.text)
                print(f'{name}的主页面获取完成!')
                # print(res.text)
                tree_phone = etree.HTML(res_phone.text)
                tree_pc = etree.HTML(res_pc.text)
                zixun = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[3]/dd/text()')[0].strip()
                print(zixun)
                zaixian = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[2]/dd/text()')[0].strip()
                print(zaixian)
                shichang = tree_phone.xpath('//*[@id="app"]/div/div/div/div[2]/div[3]/div/div/p[2]/i/text()')[0].strip()
                print(shichang)
                qijia = tree_pc.xpath('/html/body/div[6]/div[3]/div/div[2]/div/div[2]/p[1]/span/text()')[0].strip()
                print(qijia)
                haoping = tree_pc.xpath('/html/body/div[6]/div[1]/div/div/div/span[2]/text()')
                if haoping:
                    haoping = haoping[0].strip()
                else:
                    haoping = ''
                print(haoping)
                pingjiashu = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[4]/dd/text()')[0].strip()
                print(pingjiashu)
                pingjiaxingji = tree_pc.xpath('/html/body/div[6]/div[1]/div/div/div/span[1]/text()')[0].strip()
                print(pingjiaxingji)
                congyenianxian = tree_pc.xpath('/html/body/div[6]/div[2]/div/div/dl[1]/dd/text()')[0].strip()
                print(congyenianxian)
                # jiaoyubeijing = tree_phone.xpath('//div[@class="line_con_edu"]/p//text()')[0].strip()
                # print(jiaoyubeijing)
                # zhuanyezizhi = tree_phone.xpath('//p[@class="line_con_pro"]//text()')[0].strip()
                # print(zhuanyezizhi)

                # 专家姓名、性别、咨询数、在线帮助人数、总时长、起价、好评率、评价条数、评价星级、从业年限、教育背景、专业资质
                sheet[f'A{j}'] = name
                sheet[f'B{j}'] = '男'
                sheet[f'C{j}'] = zixun
                sheet[f'D{j}'] = zaixian
                sheet[f'E{j}'] = shichang
                sheet[f'F{j}'] = qijia
                sheet[f'G{j}'] = haoping
                sheet[f'H{j}'] = pingjiashu
                sheet[f'I{j}'] = pingjiaxingji
                sheet[f'J{j}'] = congyenianxian
                # sheet[f'K{j}'] = pingjia
                # sheet[f'L{j}'] = pingjia
                print(f'{name}下载完毕!')

                j += 1

    wb.save('ydl.xlsx')


def main():
    parse_and_save_data()


if __name__ == '__main__':
    main()
