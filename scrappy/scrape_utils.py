from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class ScrapeDriver():
    def __init__(self, headless=False):
        chrome_options = Options()
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('incognito')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")

        if headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)


        driver.implicitly_wait(4)
        driver.set_page_load_timeout(5)
        driver.command_executor.set_timeout(5)

        self.driver = driver

def valid_news_line(news_line):
    return len(news_line.strip()) > 0