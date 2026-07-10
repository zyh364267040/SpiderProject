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

        soup = soup_0.find_all(attrs={'id': 'ReviewsRef'})
        for u0 in soup:
            soup_1 = u0.find_all(attrs={'class': 'noBorder empReview cf pb-0 mb-0'})
        # print(len(soup_1))
        if len(soup_1) == 0:
            break
        for u1 in soup_1:
            soup_2 = u1.find_all(attrs={'class': 'ratingNumber mr-xsm'})
            soup_3 = u1.find_all(attrs={'class': 'pt-xsm pt-md-0 css-1qxtz39 eg4psks0'})
            soup_4 = u1.find_all(attrs={'class': 'authorJobTitle middle common__EiReviewDetailsStyle__newGrey'})
            soup_5 = u1.find_all(attrs={'class': 'd-flex align-items-center mr-std'})
            soup_6 = u1.find_all('span', attrs={'data-test': 'pros'})
            soup_7 = u1.find_all('span', attrs={'data-test': 'cons'})
            soup_8 = u1.find('ul', attrs={'class': 'pl-0'})

            Score_All = soup_2[0].text  # 总体评分
            Score = ['0', '0', '0', '0', '0', '0']
            if soup_8:  # 细分评分按照顺序 work	culture	diversity	career	compensation	senior
                soup_8_li = soup_8.find_all('li')
                for i in range(0, len(soup_8_li)):
                    soup_8_li_1 = soup_8_li[i].find(attrs={'class': 'css-xd4dom e1hd5jg10'})  # 1星
                    soup_8_li_2 = soup_8_li[i].find(attrs={'class': 'css-18v8tui e1hd5jg10'})  # 2星
                    soup_8_li_3 = soup_8_li[i].find(attrs={'class': 'css-vl2edp e1hd5jg10'})  # 3星
                    soup_8_li_4 = soup_8_li[i].find(attrs={'class': 'css-1nuumx7 e1hd5jg10'})  # 4星
                    soup_8_li_5 = soup_8_li[i].find(attrs={'class': 'css-s88v13 e1hd5jg10'})  # 5星
                    if soup_8_li_1:
                        Score[i] = '1.0'
                    if soup_8_li_2:
                        Score[i] = '2.0'
                    if soup_8_li_3:
                        Score[i] = '3.0'
                    if soup_8_li_4:
                        Score[i] = '4.0'
                    if soup_8_li_5:
                        Score[i] = '5.0'
                if len(soup_8_li) != 6:
                    for i in range(len(soup_8_li), 6):
                        Score[i] = soup_2[0].text
            else:
                for i in range(0, 6):
                    Score[i] = soup_2[0].text
            if soup_3[0].text[:6] == "Former":  # 标题
                title = 'Former Employee'
            else:
                # print('标题2 Good employer')
                title = 'Good employer'

            j = 0
            for i in soup_4[0].text:
                if i == '-':
                    comments_time = soup_4[0].text[:j]  # 评论时间
                    comments_posts = soup_4[0].text[j + 2:]  # 评论职位
                    break
                j += 1
            feel = ['', '', '']
            i = 0
            for u2 in soup_5:  # 按照从上倒下依次为Recommend CEO Approval Business Outlook
                soup_5_0 = u2.find_all('span', attrs={'class': 'SVGInline css-10xv9lv d-flex'})
                soup_5_1 = u2.find_all('span', attrs={'class': 'SVGInline css-hcqxoa d-flex'})
                soup_5_2 = u2.find_all('span', attrs={'class': 'SVGInline css-1h93d4v d-flex'})
                soup_5_3 = u2.find_all('span', attrs={'class': 'SVGInline css-1kiw93k d-flex'})
                if soup_5_0:
                    feel[i] = "neutral"  # ⚪
                if soup_5_1:
                    feel[i] = "positive"  # √
                if soup_5_2:
                    feel[i] = "negative"  # -
                if soup_5_3:
                    feel[i] = "bad"  # ×
                i += 1

            Pros = soup_6[0].text  # Pros

            cons = soup_7[0].text  # cons

            final = str(Sum) + ";" + str(Score_All) + ";"
            print('final:', final)
            for i in range(0, 6):
                final += str(Score[i]) + ";"
            final += str(title) + ";" + str(comments_time) + ";" + str(comments_posts) + ";"
            for i in range(0, 3):
                final += str(feel[i]) + ";"
            final += str(Pros) + ";" + str(cons) + ";" + "\n"
            with open('1-500.txt', 'a', encoding='utf-8') as data:
                print(final, file=data)
        if len(soup_1) < 9:
            n = 0
        else:
            n += 1


def main():
    dic = {}
    with open("url.txt", 'r', encoding="utf-8")as f:
        url_0 = f.readlines()
        Sum = 30
        for file in url_0:
            dic[file] = Sum
            Sum += 1
            print(file, Sum)
    print(dic)

    with ThreadPoolExecutor(10) as t:
        for file, Sum in dic.items():
            t.submit(get_data, file, Sum)


if __name__ == '__main__':
    main()
