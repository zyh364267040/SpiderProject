from telnetlib import EC
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException, StaleElementReferenceException, TimeoutException
import pandas as pd
import time

from selenium.webdriver.support.wait import WebDriverWait


def fetch_jobs(keyword, location):
    options = Options()
    options.add_argument("window-size=1920,1080")
    # Enter chromedriver.exe path below
    chrome_path = r'/Users/zhouyanhui/Library/CloudStorage/OneDrive-个人/chromedriver'
    service = Service(executable_path=chrome_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.glassdoor.co.in/Job/Home/recentActivity.html")
    driver.maximize_window()  # maximize the window
    search_input = driver.find_element(By.ID, "sc.keyword")
    search_input.send_keys(Keys.CONTROL, 'a')  # clear the location given text
    time.sleep(1)
    search_input.send_keys(keyword)  # enter the new keywords
    # search_input.send_keys(Keys.ENTER)

    search_input_location = driver.find_element(By.ID, "sc.location")
    # clear the location given text
    search_input_location.send_keys(Keys.CONTROL, 'a')
    # enter the new keywords
    search_input_location.send_keys(location)

    time.sleep(1)
    # click the search bottom     instead of "search_input_location.send_keys(Keys.ENTER)"
    search_bottom = driver.find_element(By.XPATH, "/html/body/header/nav[1]/div/div/div/div[3]/div[2]/form/div/button")
    search_bottom.click()
    time.sleep(5)

    strings = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div/div/div/div/div[2]/section/article/div[2]/div/div[2]").text
    # update the pages
    num_pages = int(strings.split()[-1])
    # num_pages = 2
    print('totally ', num_pages, ' pages need to be scraped')
    company_name = []
    age = []
    job_title = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []

    # Set current page to 1
    current_page = 1
    time.sleep(3)

    while current_page <= num_pages:
        print('tarting scraping page:', current_page)
        # step 1 scrap the left side information
        flag = 0
        resp = driver.page_source

        soup = BeautifulSoup(resp, 'html.parser')

        allJobsContainer = soup.find("ul", {"class": "css-7ry9k1"})

        allJobs = allJobsContainer.find_all("li")
        total = 0
        for job in allJobs:
            total += 1
            try:
                str1 = job.find('div', attrs={'data-test': 'job-age',
                                              'class': 'd-flex align-items-end pl-std css-1vfumx3'}).text
                age.append(str1)
            except:

                age.append("#N/A")

            try:
                job_title.append(job.find("a", {"class": "jobLink css-1rd3saf eigr9kq2"}).text)
            except:
                job_title.append("#N/A")

            try:
                location.append(job.find("div", {"class": "d-flex flex-wrap css-11d3uq0 e1rrn5ka2"}).text)
            except:
                location.append("#N/A")

            try:
                salary_estimate.append(job.find("div", {"class": "css-3g3psg pr-xxsm"}).text)
            except:
                salary_estimate.append("#N/A")
        # reset flag done as false for entering the step 2
        done = False

        # step 2 scrape the details

        while not done:
            counter = 0
            try:
                job_cards = driver.find_elements(By.XPATH, "//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            except NoSuchElementException:
                print("did not find job_cards (NoSuchElementException) on this page", current_page)
                while counter <= total:
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    counter += 1
                current_page = 10000
                break
            except ElementNotInteractableException:
                print("did not find job_cards (ElementNotInteractableException) on this page", current_page)
                while counter <= total:
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    counter += 1
                current_page = 10000
                break

            for card in job_cards:

                counter += 1

                try:
                    card.click()
                    print('click job', counter, ' on page', current_page)
                except StaleElementReferenceException:
                    print("problem with click a card ", counter)
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    continue

                time.sleep(2)
                # Closes the signup prompt
                try:
                    driver.find_element(By.XPATH, ".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(2)
                except NoSuchElementException:
                    time.sleep(2)
                    pass

                # Expands the Description section by clicking on Show More
                try:

                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div/div["
                                                                  "2]/section/div/div/article/div/div[2]/div[1]/div/div/div[2]"))
                    )
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass

                try:
                    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div["
                                                  "2]/section/div/div/article/div/div[2]/div[1]/div/div/div[2]").click()
                    time.sleep(1)
                except NoSuchElementException:
                    print("did not find show more (NoSuchElementException) on this page", counter)
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    continue

                except ElementNotInteractableException:
                    print("did not find show more (ElementNotInteractableException) on this page", counter)
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    continue
                except ElementClickInterceptedException:
                    print("did not find show more (ElementClickInterceptedException) on this page", counter)
                    flag += 8
                    company_name.append("#N/A")
                    job_description.append("#N/A")
                    company_size.append("#N/A")
                    company_type.append("#N/A")
                    company_sector.append("#N/A")
                    company_industry.append("#N/A")
                    company_founded.append("#N/A")
                    company_revenue.append("#N/A")
                    continue
                print("data scraping~~~~~~~~~~~~")
                # Scrape
                try:
                    str1 = driver.find_element(By.XPATH,
                                               "/html/body/div[2]/div/div/div/div/div[2]/section/div/div/article/div/div[1]/div/div/div/div/div[1]/div[1]/div").text
                    company_name.append(str1)
                except:
                    company_name.append("#N/A")
                    pass

                # try:
                #     job_title.append(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div["
                #                                                    "2]/section/div/div/article/div/div["
                #                                                    "1]/div/div/div[1]/div[3]/div[1]/div[2]").text)
                # except:
                #     job_title.append("#N/A")
                #     pass

                # try:
                #     location.append(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/section/div/div/article/div/div[1]/div/div/div/div/div[1]/div[3]").text)
                # except:
                #     location.append("#N/A")
                #     pass

                try:
                    job_description.append(driver.find_element(By.XPATH, "//div[@id='JobDescriptionContainer']").text)
                except:
                    job_description.append("#N/A")
                    pass

                # try:
                #     salary_estimate.append(driver.find_element(By.XPATH, "//div[@class='css-y2jiyn e2u4hf18']").text)
                # except:
                #     salary_estimate.append("#N/A")
                #     pass

                try:
                    company_size.append(driver.find_element(By.XPATH,
                                                            "//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                except:
                    company_size.append("#N/A")
                    pass

                try:
                    company_type.append(driver.find_element(By.XPATH,
                                                            "//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append("#N/A")
                    pass

                try:
                    company_sector.append(driver.find_element(By.XPATH,
                                                              "//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append("#N/A")
                    pass

                try:
                    company_industry.append(driver.find_element(By.XPATH,
                                                                "//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append("#N/A")
                    pass

                try:
                    company_founded.append(driver.find_element(By.XPATH,
                                                               "//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append("#N/A")
                    pass

                try:
                    company_revenue.append(driver.find_element(By.XPATH,
                                                               "//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append("#N/A")
                    pass

            done = True
            if flag >= 8:
                print("need refresh the page~~~~~~~~~~~~~~~~~~~~~~~~~~   ", current_page)
                print(flag)
                driver.refresh()
                time.sleep(5)
                try:
                    driver.find_element(By.XPATH, ".//span[@class='SVGInline modal_closeIcon']").click()
                    print("colsed")
                    time.sleep(2)
                except NoSuchElementException:
                    print("col1111111111se")
                    time.sleep(2)
                    pass
        # step 3 Moves to the next page
        print("moving to the next page")
        if done:
            print(str(current_page) + ' ' + 'out of' + ' ' + str(num_pages) + ' ' + 'pages done')
            driver.find_element(By.XPATH, "//span[@alt='next-icon']").click()
            current_page = current_page + 1
            time.sleep(4)

    driver.close()
    df = pd.DataFrame({'company': company_name,
                       'job title': job_title,
                       'location': location,
                       'age': age,
                       'job description': job_description,
                       'salary estimate': salary_estimate,
                       'company_size': company_size,
                       'company_type': company_type,
                       'company_sector': company_sector,
                       'company_industry': company_industry,
                       'company_founded': company_founded,
                       'company_revenue': company_revenue})

    df.to_csv(keyword + location + '.csv')


fetch_jobs("Data", "Indiana")