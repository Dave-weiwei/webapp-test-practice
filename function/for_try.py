import os
import allure
from datetime import datetime

def use_try(driver, func, pic_name, folder="fail_screenshots"):
    # """
    # 執行 func()，若失敗則自動截圖並回報錯誤。
    
    # :param func: 一個不帶參數的函數，例如 lambda 或 def 包裝的測試動作
    # :param pic_name: 截圖命名用的識別字（例如測試名稱或 index）
    # :param driver: Selenium 的 WebDriver 實例
    # :param folder: 截圖存放的資料夾（預設為 screenshots）
    # """
    try:
        func()
    except Exception as e:

        date_folder = datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join("tests", folder, date_folder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{pic_name}.png")
        
        # 儲存截圖
        driver.save_screenshot(file_path)
        print(f"[!] 測試失敗，自動截圖已儲存：{file_path}")
        print(f"[!] 錯誤訊息：{e}")
        
        # 👉 Allure 嵌入圖片（需 allure-pytest 套件）
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                allure.attach(f.read(), name=pic_name, attachment_type=allure.attachment_type.PNG)

        raise e  # 將錯誤拋出給 pytest 判斷為失敗