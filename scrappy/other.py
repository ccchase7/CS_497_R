from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('incognito')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")

headless = False

if headless:
    chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)


driver.implicitly_wait(4)
driver.set_page_load_timeout(5)
driver.command_executor.set_timeout(5)

urls = ['https://www.mmafighting.com/2019/10/16/20917409/jon-jones-accepts-plea-deal-in-strip-club-case',' https://www.nytimes.com/2019/10/24/world/europe/ukraine-war-impeachment.html', 'https://www.techradar.com/how-to/record-your-screen', 'https://www.techradar.com/news/google-assistant-bug-stops-phone-screens-powering-off-what-you-need-to-know', 'https://www.thekitchn.com/recipe-panzanella-with-roasted-152392']
for url in urls:
    print(f"getting from {url}....")
    try:
        driver.get(url)
    except:
        print(f"Timed out.")
    try:
        print("finding....")
        all_p = driver.find_elements(By.TAG_NAME, 'p')
        print("printing...")
        for p in all_p:
            print(p.text)
    except Exception as e:
        print(e)
    
    #print("A BIG exception done happened. We Quittin'")
    #finally:
        #pass
driver.quit()

