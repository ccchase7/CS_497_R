from scrape_utils import *
from utils import *
from NewsItem import NewsItem
import json

output_file = "newsItemJson.txt"
input_url_file = "tempJson.txt"

with open(input_url_file, "r") as inFile:
    lines = inFile.read().splitlines()

search_results = [json_to_SearchResult(line) for line in lines if len(line.strip())]

#urls = ['https://www.mmafighting.com/2019/10/16/20917409/jon-jones-accepts-plea-deal-in-strip-club-case',' https://www.nytimes.com/2019/10/24/world/europe/ukraine-war-impeachment.html', 'https://www.techradar.com/how-to/record-your-screen', 'https://www.techradar.com/news/google-assistant-bug-stops-phone-screens-powering-off-what-you-need-to-know', 'https://www.thekitchn.com/recipe-panzanella-with-roasted-152392']

for search_result in search_results:
    driver = ScrapeDriver(headless=False).driver
    curr_url = search_result.article_url
    print(f"getting from {curr_url}....")
    try:
        try:
            driver.get(curr_url)
        except:
            print(f"Timed out.")
    
        print("finding....")
        all_p = driver.find_elements(By.TAG_NAME, 'p')
        print("printing...")
        for p in all_p:
            print(p.text)

        curr_news_item = NewsItem(driver.title, search_result, "\n".join([p.text for p in all_p if valid_news_line(p.text)]))
        print(curr_news_item)

        with open(output_file, "a") as outFile:
            #outFile.write(f"{json.dumps(curr_news_item.__dict__)}\n")
            outFile.write(f"{curr_news_item.toJson()}\n")

    except Exception as e:
        print(e)

    finally:
        driver.quit()

