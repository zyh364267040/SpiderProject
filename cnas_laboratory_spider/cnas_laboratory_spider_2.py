# -*- coding = utf-8 -*-
# @Time: 2022/10/7 16:07
import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from lxml import etree
import requests
import openpyxl


def main():
    # 创建excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = '名称'
    sheet['B1'] = '联系人'
    sheet['C1'] = '电话'
    sheet['D1'] = '网址'
    sheet['E1'] = '地址'
    i = 2

    # 创建webdriver对象
    driver = webdriver.Chrome('/Users/zhouyanhui/Library/CloudStorage/OneDrive-个人/chromedriver')

    # 发送请求
    url = 'https://las.cnas.org.cn/LAS_FQ/publish/externalQueryL1.jsp'
    driver.get(url)
    time.sleep(0.5)

    # 输入关键字和选项
    driver.find_element(By.XPATH, '//*[@id="orgAddress"]').send_keys('深圳')
    time.sleep(0.5)
    s1 = Select(driver.find_element(By.XPATH, '//*[@id="orgAreaSel"]'))
    s1.select_by_value('01')
    time.sleep(0.5)
    # 点击查询
    driver.find_element(By.XPATH, '//*[@id="mainForm"]/fieldset/div[6]/input[2]').click()
    time.sleep(0.5)

    # 循环请求7页数据
    for j in range(7):
        # 手动输入验证码
        verify = input('请输入验证码:')
        # 输入验证码,点击确认
        driver.find_element(By.XPATH, '//*[@id="authInterceptVName"]').send_keys(verify)
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="pirlbutton1"]').click()
        time.sleep(10)

        # 获取源码,并使用xpath获取每个网页url
        tree = etree.HTML(driver.page_source)
        trs = tree.xpath('//tbody[@class="yui-dt-data"]/tr')

        # 循环每一个连接,并请求
        for tr in trs:
            onclick = tr.xpath('./td[2]/div/a/@onclick')
            onclick = onclick[0].replace('_showTop(\'', '').replace('\');', '')
            # print(onclick)

            # 请求每一项网页信息
            for aa in range(5):
                try:
                    url = f'https://las.cnas.org.cn{onclick}&authInterceptCode={verify}'
                    print(url)
                    res = requests.get(f'https://las.cnas.org.cn{onclick}&authInterceptCode={verify}', timeout=10)
                    if res:
                        break
                except Exception as e:
                    print(e)
            # print(res.text)
            # 获取网页数据后,使用xpath获取数据
            tree = etree.HTML(res.text)

            name = tree.xpath('//div[@class="T1"]/text()')
            # 判断数据是存在,如果存在获取,不存在默认空值
            if name:
                name = name[0]
            else:
                name = ''

            people = tree.xpath('/html/body/div[1]/table[1]/tr[3]/td[1]/span/text()')
            if people:
                people = people[0]
            else:
                people = ''

            tel = tree.xpath('/html/body/div[1]/table[1]/tr[3]/td[2]/span/text()')
            if tel:
                tel = tel[0]
            else:
                tel = ''

            web_address = tree.xpath('/html/body/div[1]/table[1]/tr[5]/td[1]/span/a/text()')
            if web_address:
                web_address = web_address[0]
            else:
                web_address = ''

            address = tree.xpath('/html/body/div[1]/table[1]/tr[6]/td/span/text()')
            if address:
                address = address[0]
            else:
                address = ''

            print(name, people, tel, web_address, address)

            # 将获取到的信息保存到excel
            sheet[f'A{i}'] = name
            sheet[f'B{i}'] = people
            sheet[f'C{i}'] = tel
            sheet[f'D{i}'] = web_address
            sheet[f'E{i}'] = address
            i += 1

            time.sleep(random.choice([1, 2, 3]))

        if j < 6:
            # 点击进入下一页
            driver.find_element(By.XPATH, '//*[@id="yui-pg0-0-next-link"]').click()
            time.sleep(0.5)

    # 保存数据到文件
    wb.save('cnas.xlsx')


if __name__ == '__main__':
    main()
