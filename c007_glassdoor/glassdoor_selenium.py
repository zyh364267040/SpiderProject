from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GlassDoor:

    def __init__(self, webdriver_path):
        self.driver = webdriver.Chrome(webdriver_path)

    def login(self, username, password):
        login_url = 'https://www.glassdoor.com/index.htm'
        self.driver.get(login_url)
        try:
            username_input = self.driver.find_element(By.ID, 'userEmail')
        except Exception:
            username_input = self.driver.find_element(By.ID, 'inlineUserEmail')
        username_input.send_keys(username)

        time.sleep(0.5)

        continue_with_email = self.driver.find_element(By.CLASS_NAME, 'css-8zxfjs')
        continue_with_email.click()

        time.sleep(5)

        # password_input = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'inlineUserPassword'))
        # )
        password_input = self.driver.find_element(By.ID, 'inlineUserPassword')
        password_input.send_keys(password)

        time.sleep(0.5)

        sign_in = self.driver.find_element(By.CLASS_NAME, 'css-8zxfjs')
        sign_in.click()

        time.sleep(10)


webdriver_path = '/Users/zhouyanhui/Library/CloudStorage/OneDrive-个人/chromedriver'
glass_door = GlassDoor(webdriver_path)
glass_door.login(username='759388790@qq.com', password='erhui7169')
