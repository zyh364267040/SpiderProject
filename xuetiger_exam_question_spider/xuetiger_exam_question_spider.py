# -*- coding: utf-8 -*-
# @Time: 2022/9/4 21:11
"""学虎网在线题库题目采集脚本。

说明：原始代码中的历史登录凭据已删除。
如需运行，请按当前网站要求自行配置合法访问参数，并遵守网站规则。
"""
import requests
import random
from lxml import etree


def post_data(number):
    # url
    url = f'http://www.xuetiger.com/index.php?exam-app-lesson-ajax-questions&knowsid=6&number={number}'

    # headers
    # 原始旧登录凭据已删除，避免泄露历史访问凭据。
    # 如果当前网站需要登录，请按合法方式自行补充访问参数。
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Referer': 'http://www.xuetiger.com/index.php?exam-app-lesson-paper&knowsid=6'
    }

    # form_data
    data = {
        'userhash': random.random()
    }

    # 发送post请求,获取数据
    for i in range(10):
        print(i)
        try:
            res = requests.post(url, data=data, headers=headers)
        except Exception as e:
            print(f'请求发生错误,正在进行第{i+1}次重试...')
            print(e)
        else:
            return res


def parse_data(res, number):
    # 新建存储文件
    f = open('xuetiger_exam_questions.txt', 'a', encoding='utf-8')

    # 解析HTML
    html = etree.HTML(res.text)
    # 获取题目
    ques = html.xpath('/html/body/ul/li[1]/div/p/text()')[0]
    ques = f'第{number}题: {ques}'
    f.write(ques + '\n')
    print(ques)

    # 获取答案
    ans = html.xpath('/html/body/ul/li[2]/div/p/text()')
    for an in ans:
        f.write(an + '\n')
        print(an)

    # 获取正确答案
    ture_ans = html.xpath('/html/body/ul/li[4]/div/div/div[2]/b/text()')[0]
    ture_ans = f'正确答案: {ture_ans}'
    f.write(ture_ans + '\n')
    print(ture_ans)

    # 关闭文件
    f.close()


def main():
    for number in range(1, 10):
        # number = 1001
        # 1. 发送请求,获取数据
        res = post_data(number)

        # 2. 解析数据,保存
        parse_data(res, number)


if __name__ == '__main__':
    main()
