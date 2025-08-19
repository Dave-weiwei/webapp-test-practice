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
        
    def verify_input_default(self, by, target, source):
        if source == "placeholder":
            default_value=self.driver.find_element(by,target).get_attribute("placeholder")
            return default_value
        elif source == "value":
            default_value=self.driver.find_element(by,target).get_attribute("value")
            return default_value
        else:
            default_value=self.driver.find_element(by,target).text
            return default_value

    
    def click(self, by, target):
            item = self.driver.find_element(by, target)
            if by == By.LINK_TEXT:
                item.click()
                self.driver.switch_to.window(self.driver.window_handles[1])
                show = self.driver.current_url
                return show
            else:
                item.click()
                show= self.driver.find_element(By.ID,"show").get_attribute("value")
                return show

    def select(self, sel_item):
        sel = Select(self.driver.find_element(By.ID, 'select'))
        sel.select_by_index(sel_item)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))",self.driver.find_element(By.ID, 'select'))
        sel_set = sel.first_selected_option.text
        WebDriverWait(self.driver, 3).until(lambda d: d.find_element(By.ID, "show").get_attribute("value") == sel_set)
        show = self.driver.find_element(By.ID, "show").get_attribute("value")
        return sel_set, show

    def input_send(self,input):
        input_key=self.driver.find_element(By.ID,"name")
        input_key.send_keys(input)
        btn = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        btn.click()
        WebDriverWait(self.driver , 3).until(EC.visibility_of_element_located((By.ID, "submit-status")))
        status = self.driver.find_element(By.ID,"submit-status").get_attribute("textContent")
        return status

    def reg(self, username, password, confirm):
        user_input = self.driver.find_element(By.ID, "reg-username")
        user_pwd = self.driver.find_element(By.ID, "reg-password")
        pwd_confirm = self.driver.find_element(By.ID, "reg-confirm")
        sub_btn = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="註冊"]')
        user_input.send_keys(username)
        user_pwd.send_keys(password)
        pwd_confirm.send_keys(confirm)
        sub_btn.click()
        valid_u = self.driver.execute_script("return document.getElementById('reg-username').checkValidity();")
        valid_p = self.driver.execute_script("return document.getElementById('reg-password').checkValidity();")
        valid_c = self.driver.execute_script("return document.getElementById('reg-confirm').checkValidity();")
        if all([valid_u, valid_p, valid_c]):
            WebDriverWait(self.driver, 3).until(lambda d: d.find_element(By.ID, "register-result").text != "")
            reg_result= self.driver.find_element(By.ID, "register-result").text
            print("[DEBUG] register-result:", reg_result)
            if reg_result == "註冊成功":
                return True
            else:
                return False
        else:
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
    