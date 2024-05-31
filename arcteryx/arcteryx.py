# -*- coding = utf-8 -*-
# @Time: 2022/11/1 18:52
import requests
import time
import random
from lxml import etree
import re
from urllib.parse import urljoin
from selenium import webdriver
import json


# options = webdriver.ChromeOptions()
# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
# options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# # 隐藏窗口
# options.add_argument('headless')
# driver = webdriver.Chrome('/Users/zhouyanhui/Library/CloudStorage/OneDrive-个人/chromedriver', options=options)


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
                with open('shibai.txt', 'w', encoding='utf-8') as f:
                    f.write(url + '\n')


def parse_data(res):
    # print(res.text)
    # 使用正则匹配男装数据
    pattern1 = r'P=function\(e\){(.*?)},T=function'
    result = re.findall(pattern1, res.text)

    pattern2 = r'<a href="(.*?)"'
    men_href_list = re.findall(pattern2, result[0])

    # 使用正则匹配女装数据
    pattern3 = r'<span data-prefix="women">\'\).concat\(e.Clothing(.*?)data-prefix="women" data-linkid="women:clothing:shorts">'
    result = re.findall(pattern3, res.text)

    pattern4 = r'<a href="(.*?)"'
    women_href_list = re.findall(pattern4, result[0])

    href_list = men_href_list + women_href_list

    for href in href_list:
        href = href.split('/')[-2].replace('-', '')
        url = 'https://arcteryx.com/us/en/api/fredhopper/query?fh_location=//catalog01/en_CA/categories<{' + href + '}/gender>{mens}&fh_country=us&fh_refview=lister&fh_view_size=all&fh_context_location=//catalog01'
        des_res = get_data(url)
        parse_des_res(des_res)


def parse_des_res(res):
    # 使用正则获取数据
    pattern = r'item":(.*?)}},"themes'
    result = re.findall(pattern, res.text)[0]
    # print(result)

    first_url = 'https://arcteryx.com/us/en/shop/'

    # 转成列表
    result_list = json.loads(result)
    for result in result_list:
        value = result['attribute'][5]['value'][0]['value']

        # 商品名
        name = result['attribute'][26]['value'][0]['value']

        # 价格
        jiage = result['attribute'][25]['value'][0]['value']

        # 颜色
        color_list = result['attribute'][13]['value']
        yanse = []
        for color in color_list:
            yanse.append(color['value'])
        yanse = ' '.join(yanse)
        # print(yanse)

        url = urljoin(first_url, value)
        clothes_res = get_data(url)
        parse_clothes_data(clothes_res, name, jiage, yanse)


def parse_clothes_data(res, name, jiage, yanse):
    print(res.text)
    # 正则
    pattern = r'modelMetricsExtra(.*?)Arc\'teryx Layering Guide'
    result = re.findall(pattern, res.text)

    pattern2 = r'features":(.*?),"bigWidgets'
    result2 = re.findall(pattern2, result[0].replace('\\', ''))

    info_list = json.loads(result2[0])
    technical_features = ''
    construction = ''
    cuff = ''
    design = ''
    fabric = ''
    hood = ''
    patterning = ''
    pocket = ''
    snowsport = ''
    sustainability = ''
    zippers = ''
    for info in info_list:
        if info['label'] == 'Technical Features':
            technical_features = ' '.join(info['value'])
        if info['label'] == 'Construction':
            construction = ' '.join(info['value'])
        if info['label'] == 'Cuff u0026 Sleeves Configuration':
            cuff = ' '.join(info['value'])
        if info['label'] == 'Design u0026 Fit':
            design = ' '.join(info['value'])
        if info['label'] == 'Fabric Treatment':
            fabric = ' '.join(info['value'])
        if info['label'] == 'Hood Configuration':
            hood = ' '.join(info['value'])
        if info['label'] == 'Patterning':
            patterning = ' '.join(info['value'])
        if info['label'] == 'Pocket Configuration':
            pocket = ' '.join(info['value'])
        if info['label'] == 'Snowsport Features':
            snowsport = ' '.join(info['value'])
        if info['label'] == 'Sustainability':
            sustainability = ' '.join(info['value'])
        if info['label'] == 'Zippers u0026 Fly Configuration':
            zippers = ' '.join(info['value'])

    # 用xpath方法获取数据
    tree = etree.HTML(res.text)
    div_list = tree.xpath('//*[@id="content"]/section[6]/div')

    size = ''
    weight = ''
    fit = ''
    model_measurements = ''
    sizing_chart = ''
    activity = ''
    model = ''
    manufacturing_facility = ''
    for div in div_list:
        text = div.xpath('./strong/text()')
        value = div.xpath('./span//text()')

        # size
        if 'Size' in text:
            size = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # weight
        if 'Weight' in text:
            weight = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # fit
        if 'Fit' in text:
            fit = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # Model Measurements
        if 'Model Measurements' in text:
            model_measurements = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # Sizing Chart
        if 'Sizing Chart' in text:
            sizing = div.xpath('./a//text()')
            if sizing:
                sizing_chart = sizing[0].replace(',', '，').replace(' ', '').strip()
                continue

        # Activity
        if 'Activity' in text:
            activity = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # Model
        if 'Model' in text:
            model = value[0].replace(',', '，').replace(' ', '').strip()
            continue

        # Manufacturing Facility
        if 'Manufacturing Facility' in text:
            manufacturing = div.xpath('./a//text()')
            if manufacturing:
                manufacturing_facility = manufacturing[0].replace(',', '，').replace(' ', '').strip()
                continue

    # 详情图
    img_list = []
    button_list = tree.xpath('//section[@id="product-detail-images"]/div/button')
    for button in button_list[:5]:
        data_src = button.xpath('./figure/img/@data-src')
        if not data_src:
            continue
        data_src = data_src[0]
        img_list.append(data_src)
    img = '，'.join(img_list)

    # 详情介绍
    describe = tree.xpath('//*[@id="product-description"]/div/text()')
    if not describe:
        describe = tree.xpath('//*[@id="product-description"]/div/p/text()')
    if not describe:
        describe = tree.xpath('//*[@id="product-description"]/div/p[1]/text()')
    if describe:
        describe = describe[0]
        describe = describe.replace(',', '，')
        describe = describe.strip()

    # 产品分类
    fenlei = ''
    fenlei_list = tree.xpath('//*[@id="breadcrumb"]/nav/div//text()')
    for fenlei in fenlei_list:
        if 'Men\'s' in fenlei:
            index = fenlei_list.index(fenlei)
            fenlei = fenlei_list[index] + '>' + fenlei_list[index + 1]
            break

    print(name, jiage, yanse, size, img, describe, fenlei, weight, fit, model_measurements, sizing_chart, activity,
          model, manufacturing_facility, technical_features, construction, cuff, design, fabric, hood, patterning,
          pocket, snowsport, sustainability, zippers)
    with open('clothes.txt', 'a', encoding='utf-8') as f:
        f.write(f'{name}@{jiage}@{yanse}@{size}@{img}@{describe}@{fenlei}@{weight}@{fit}@{model_measurements}@'
                f'{sizing_chart}@{activity}@{model}@{manufacturing_facility}@{technical_features}@{construction}@{cuff}@'
                f'{design},{fabric}@{hood}@{patterning}@{pocket}@{snowsport}@{sustainability}@{zippers}\n')


def main():
    # 存储数据文件
    with open('clothes.txt', 'w', encoding='utf-8') as f:
        f.write(
            '商品名,价格,颜色,尺寸,详情图,详情介绍,产品分类,Weight,Fit,Model Measurements,Sizing Chart,Activity,Model,'
            'Manufacturing Facility,Technical Features,Construction,Cuff & Sleeves Configuration,Design & Fit,'
            'Fabric Treatment,Hood Configuration,Patterning,Pocket Configuration,Snowsport Features,Sustainability,'
            'Zippers & Fly Configuration\n'
        )
    url = 'https://ui-components.arcteryx.com/us/en/outdoorHeader.js'
    res = get_data(url)
    parse_data(res)


if __name__ == '__main__':
    main()
