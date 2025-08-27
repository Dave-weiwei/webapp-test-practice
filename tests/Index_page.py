from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

class IndexPage:
    def __init__(self,driver):
        self.driver=driver
        base = os.getenv("BASE_URL", "http://127.0.0.1:5000/")
        if not base.startswith("http"):
            base = "http://" + base
        if not base.endswith("/"):
            base += "/"
        self.url = base
        
    def open(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver , 3).until(EC.presence_of_element_located((By.CSS_SELECTOR,'h1[title="我是大標題"]')))
        
    def verify_element_exists(self, by, target):
        try:
            self.driver.find_element(by,target)
            return True
        except:
            return False
        
    
    
    

    def login(self, username, password):
        user_input = self.driver.find_element(By.ID, "login-username")
        user_pwd = self.driver.find_element(By.ID, "login-password")
        sub_btn = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="登入"]')

        user_input.send_keys(username)
        user_pwd.send_keys(password)
        sub_btn.click()
        WebDriverWait(self.driver, 3).until(lambda d: d.find_element(By.ID,"login-result").text != "")
        show = self.driver.find_element(By.ID,"login-result").text
        return show       
    