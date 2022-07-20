from selenium import webdriver
from selenium.webdriver.common.by import By


class Test_login_logout:

    def __init__(self, url):
        self.driver = webdriver.Chrome()
        print("Chrome was open")
        self.driver.get(url)
        print('Page was open')

    def go_to_login(self):
        go_login_button = self.driver.find_element(By.ID, 'login_button')
        go_login_button.click()
        print('Now at login page')

    def login(self, email, psw):
        login_input = self.driver.find_element(By.ID, 'floatingInput')
        login_input.send_keys(email)
        psw_input = self.driver.find_element(By.ID, 'floatingPassword')
        psw_input.send_keys(psw)
        login_button = self.driver.find_element(By.CLASS_NAME, 'w-100.btn.btn-lg.btn-primary')
        login_button.click()
        print('Was login')

    def logout(self):
        select = self.driver.find_element(By.ID, 'dropdown')
        select.click()
        logout_btn = self.driver.find_element(By.ID, 'logout_btn')
        logout_btn.click()
        print('Was logout')

    def __del__(self):
        self.driver.close()
        print('Chrome was closed')
