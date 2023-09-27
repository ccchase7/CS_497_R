from Requests import Requester
from Parses import Parser
from utils import *
from bs4 import BeautifulSoup as bs
from time import sleep

NUM_TITLES_TO_PROCESS = 2500
to_file = False
outFile = "output.txt"
outFolder = "outFolder"

requester = Requester()

dom_path_dict = {"YAHOO!News": ["div:caas-body", "p"], "Yahoo": ["div:caas-body", "p"], "MSN": ["article"]}

queries = ["How to record your screen on Windows, macOS, iOS or Android"]
#queries = ["The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
#queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)

# Concatenate all the words, and replace special characters.
#queries = ("+".join(searchify_news_title(i).split()) for i in queries)
concat_symbs = ["+", "-"]

valid_urls = []
count = 0

for query in queries:
    try:
        count += 1
        if count % 10 == 0:
            print(f"Count: {count}")

        results_list = []

        for concat_symb in concat_symbs:
            print(query)
            temp_query = format_query(f"{concat_symb}".join(searchify_news_title(query).split()))
            print(f"{temp_query}")
            search_dom = requester.get_request(temp_query)
            b = bs(search_dom.text, 'html.parser')
            results_list = b.find_all("li", class_="b_algo")
            
            if len(results_list) > 0:
                for result in results_list:
                    search_result = bs(str(result), 'html.parser')
                    date = search_result.find_all('span', class_="news_dt")
                    if not in_date_range(date[0].text):
                        continue

                    additional_info = search_result.find_all('h2')
                    title_and_source = bs(str(additional_info), 'html.parser')

                    title_and_source = title_and_source.find_all('strong')
                    print(f"Title and Source: {[info.text for info in title_and_source]}")
                    print(f"Date: {date[0].text}")
                    curr_url = extract_Url_From_Href(result)
                    #print(f"URL: {curr_url}")
                    valid_urls.append(curr_url)
                    #curr_news_source = extract_News_Source(first_result)
            else:
                if to_file:
                    with open(f"{outFolder}/htmls/request{count}.html", "w") as f2:
                        f2.write(b.prettify())

                    with open(f"{outFolder}/queries.txt", "a") as f3:
                        f3.write(f"{count}: {temp_query}\n")

        #sleep(.1)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"An exception occurred: {e}")
        pass

    print(f"Valid Urls:")
    with open(f"{outFolder}/valid_urls.txt", "a") as f4:
        for ur in valid_urls:
            print(ur)
            f4.write(f"{ur}\n")
    
    

