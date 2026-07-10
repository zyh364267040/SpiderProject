# -*- coding: utf-8 -*-
"""PhenoScanner SNP/GWAS 关联数据采集脚本。

从 CSV 读取 SNP 编号，查询 PhenoScanner GWAS 数据，提取 SNP、Trait、PMID、Beta 和 P 值并保存为 CSV。
历史访问会话信息已删除。
"""
# @Time: 2022/4/9 下午5:03
import pandas as pd
import numpy as np
import requests
from lxml import etree
import time
import random


def read_csv():
    print('开始读取csv文件数据...')
    # 文件存储路径
    file_path = 'BAOLU_exp1.csv'
    # 使用pandas读取数据
    data = pd.read_csv(file_path)
    # 获取SNP列数据
    snp = data[['SNP']]
    # 将DataFrame数据转成array
    snp_array = np.array(snp)
    # 将array转成list
    snp_list = snp_array.tolist()

    print('csv文件数据读取成功!!!')
    print('读取后的数据是:', snp_list)

    return snp_list


def get_data(data_list):
    print('开始发送关键字,获取数据...')
    num = str(len(data_list))
    print(f'共有{num}个关键字!!!')

    # 存储数据的文件
    data_f = open('data.csv', 'w')

    data_f.write('SNP,Trait,PMID,Beta,P' + '\n')

    # 循环取出搜索关键字
    for data in data_list:
        key_word = data[0]
        key_word_num = str(data_list.index(data) + 1)
        print(f'正在请求第{key_word_num}个关键字:', key_word)

        # headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'Referer': 'http://www.phenoscanner.medschl.cam.ac.uk/',
        }

        # url = 'http://www.phenoscanner.medschl.cam.ac.uk/?query=rs187786174&catalogue=GWAS&p=1e-5&proxies=None&r2=0.8&build=37'
        url = f'http://www.phenoscanner.medschl.cam.ac.uk/?query={key_word}&catalogue=GWAS&p=1e-5&proxies=None&r2=0.8&build=37'

        for i in range(10):
        #     # 发送请求获取响应
            res = requests.get(url, headers=headers)
        #     # 状态码检测是否访问成功
            if res.status_code == 200:
                # 3. 解析数据
                html = etree.HTML(res.text)
                # 使用xpath获取tr
                tr_list = html.xpath('//*[@id="myTable"]/tbody/tr')
                # 从tr中获取数据
                for tr in tr_list:
                    SNP = tr.xpath('./td[1]/text()')[0]
                    Trait = tr.xpath('./td[6]/text()')[0]
                    PMID = tr.xpath('./td[8]/text()')[0]
                    Beta = tr.xpath('./td[9]/text()')[0]
                    P = tr.xpath('./td[10]/text()')[0]

                    # 4. 保存数据到csv
                    # 将获取到的数据写入文件
                    data_f.write(SNP + ',' + Trait + ',' + PMID + ',' + Beta + ',' + P + '\n')

                    print('获取的数据是:', SNP, Trait, PMID, Beta, P)

                print(f'第{key_word_num}个关键字:{key_word}获取成功!!!')
                break
            else:
                num = str(i+1)
                print(f'请求失败,正在第{num}次重试...')

        # 访问一次后,程序强制暂停几秒
        time_num = random.randint(2, 3)
        time.sleep(time_num)

    print('全部获取完毕,GOOD BYE!!!')
    # 关闭文件
    data_f.close()


def main():
    # 1. 读取csv数据,返回要爬取的数据
    data_list = read_csv()

    # 2. 使用requests访问网站,获取数据
    get_data(data_list)


if __name__ == '__main__':
    main()
