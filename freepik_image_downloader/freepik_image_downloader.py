# -*- coding = utf-8 -*-
# @Time: 2022/9/17 21:09
import requests
import os
from lxml import etree


def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    # url = 'https://www.freepik.com/search?author=1261308&authorSlug=onlyyouqj&format=author&query=Women%20s%20fashion%20store%20in%20shopping%20center'
    url = 'https://www.freepik.com/search?author=1261308&authorSlug=onlyyouqj&format=author&page=2&query=Women+s+fashion+store+in+shopping+center'
    res = requests.get(url, headers=headers)
    # if not os.path.exists('html'):
    #     os.mkdir('html')
    # with open('./html/' + url.split('/')[-1] + '.html', 'w', encoding='utf-8') as f:
    #     f.write(res.text)

    # print(res.text)
    return res


def parse_data(res):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    tree = etree.HTML(res.text)
    img_srcs = tree.xpath('//section[@class="showcase mg-none-i"]/div/figure/div/a/img/@data-src')
    for img_src in img_srcs:
        img_src = img_src.split('?')[0] + '?w=2000 2000w'
        res = requests.get(img_src, headers=headers)
        if not os.path.exists('img'):
            os.mkdir('img')
        with open('./img/' + img_src.split('?')[0].split('/')[-1], 'wb') as f:
            f.write(res.content)
        print(f'{img_src}下载完成!')


def main():
   res = get_data()
   parse_data(res)


if __name__ == '__main__':
    main()
