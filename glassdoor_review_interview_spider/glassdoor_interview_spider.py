from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor


def get_data(file, Sum):
    s = Service(executable_path=r'E:\python\chromedriver.exe')
    driver = webdriver.Chrome(service=s)  # 驱动的路径
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)  # 这两种设置都进行才有效

    url_each = file.strip('\n')
    n = 1
    while n != 0:
        url = url_each[:len(url_each) - 4] + "_P" + str(n) + ".htm"
        try:  # 尝试打开网址，超时或者什么异常后退出
            driver.get(url)
        except:
            driver.execute_script('window.stop()')
        html = driver.page_source
        soup_0 = BeautifulSoup(html, 'lxml')

        soup = soup_0.find_all('div', attrs={'data-test': "InterviewList"})
        for u0 in soup:
            soup_1 = u0.find_all('div', attrs={'class': "mt-0 mb-0 my-md-std p-std gd-ui-module css-cup1a5 ec4dwm00"})
        print(len(soup_1))
        if len(soup_1) == 0:
            break
        for u1 in soup_1:
            soup_2 = u1.find_all('time')
            time = soup_2[0].text

            soup_3 = u1.find('a')
            title_1 = soup_3[0].text

            soup_4 = u1.find('p', attrs={'class': "mt-0 mb css-13r90be e1lscvyf1"})
            title_2 = soup_4.text

            oe3 = ['0', '0', '0']
            soup_5 = u1.find_all('span', attrs={'class': "mb-xxsm"})
            for i in range(0, len(soup_5)):
                oe3[i] = soup_5[i].text
            if len(soup_5) != 3:
                for i in range(len(soup_5), 3):
                    oe3[i] = '0'

            soup_6 = u1.find('p', attrs={'class': "mt-xsm mb-std"})
            application = soup_6.text  # application

            soup_7_0 = u1.find('p', attrs={'class': " css-w00cnv mt-xsm mb-std"})
            soup_7_1 = u1.find('p', attrs={'class': "css-lyyc14 css-w00cnv mt-xsm mb-std"})
            if soup_7_0:
                content = soup_7_0.text  # 面试内容
            if soup_7_1:
                content = soup_7_1.text

            soup_8 = u1.find('span', attrs={'class': "d-inline-block mb-sm"})
            question = soup_8.text  # 面试问题

            final = str(Sum) + ";" + str(time) + ";" + str(title_1) + ";" + str(title_2) + ";"
            for i in range(0, 3):
                final += str(oe3[i]) + ";"

            final += str(application) + ";" + str(content) + ";" + str(question) + ";" + "\n"
            with open('inte.txt', 'a', encoding='utf-8') as data:
                print(final, file=data)
        if len(soup_1) < 10:
            n = 0
        else:
            n += 1


def main():
    with open("url_int.txt", 'r', encoding="utf-8")as f:
        url_0 = f.readlines()
        Sum = 1
        dic = {}
        for file in url_0:
            dic[file] = Sum
            Sum += 1

    with ThreadPoolExecutor(10) as t:
        for file, Sum in dic.items():
            t.submit(get_data, file, Sum)


if __name__ == '__main__':
    main()
