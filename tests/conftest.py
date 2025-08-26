import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--mybrowser",
        action="store",
        default="chrome",
        help="指定瀏覽器: chrome 或 firefox"
    )

@pytest.fixture(scope="module")
def driver(request):
    browser = request.config.getoption("--mybrowser")

    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--window-size=1920,1080")
        service = ChromeService("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=firefox_options)

    else:
        raise ValueError(f"❌ 不支援的瀏覽器: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()