# -*- coding = utf-8 -*-
# @Time: 2022/10/7 15:27
# 历史会话凭据已删除；运行时由当前合法会话获取验证码和访问状态。
import random
import time
from selenium import webdriver
import requests


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    return res


def main():
    for i in range(7):
        get_url = f'https://las.cnas.org.cn/LAS_FQ/verify/getValidateCode.action?fleshCode={random.uniform(0, 1)}'
        res = get_data(get_url)
        with open('verify.png', 'wb') as f:
            f.write(res.content)

        verify = input('请输入验证码:')
        post_url = f'https://las.cnas.org.cn/LAS_FQ/verify/verifyCode.action?fleshCode={random.uniform(0, 1)}'
        data = {
            'verifyCode': verify
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://las.cnas.org.cn/LAS_FQ/publish/externalQueryL1.jsp',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '15',
            'Origin': 'https://las.cnas.org.cn',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        res = requests.post(post_url, data=data, headers=headers)
        print(res.json())
        time.sleep(1)

        post_url2 = 'https://las.cnas.org.cn/LAS_FQ/publish/queryPublishLicenseList.action?'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        data2 = {
            'labType': 'L',
            'choType': 'L',
            'orgState': 0,
            'searchLang': 'CH',
            'orgAddress': '深圳',
            'orgAreaSel': '01',
            'authInterceptCode': verify,
            'startIndex': i * 100,
            'sizePerPage': 100
        }
        res = requests.post(post_url2, data=data2, headers=headers)
        print(res.json())
        break


if __name__ == '__main__':
    main()
