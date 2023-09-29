from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from scrape_utils import *
from utils import *
from NewsItem import NewsItem
import json

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

def scrape_page(search_result):
    output_file = "ynewsItemJson.txt"

    driver = ScrapeDriver(headless=True).driver
    curr_url = search_result.article_url
    try:
        try:
            driver.get(curr_url)
        except:
            pass
    
        all_p = driver.find_elements(By.TAG_NAME, 'p')

        curr_news_item = NewsItem(driver.title, search_result, "\n".join([p.text for p in all_p if valid_news_line(p.text)]))

        with open(output_file, "a") as outFile:
            outFile.write(f"{curr_news_item.toJson()}\n")

    except Exception as e:
        pass

    finally:
        driver.quit()