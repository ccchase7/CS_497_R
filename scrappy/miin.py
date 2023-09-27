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

#queries = ["A little snow causes a big mess, more than 100 crashes on Minnesota roads", "The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
#queries = ["The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)

# Concatenate all the words, and replace special characters.
#queries = ("+".join(searchify_news_title(i).split()) for i in queries)
concat_symbs = ["+", "-", ""]

valid_urls = []
count = 0
with open(outFile, 'a') as f1:
    for query in queries:
        try:
            count += 1
            if count % 10 == 0:
                print(f"Count: {count}")

            results_list = []

            for concat_symb in concat_symbs:
                temp_query = format_query(f"{concat_symb}".join(searchify_news_title(query).split()))
                print(f"{temp_query}")
                search_dom = requester.get_request(temp_query)
                b = bs(search_dom.text, 'html.parser')
                results_list = b.find_all("h2")

                # Extract the url and news source from the first search result
                if len(results_list) > 0:
                    print(results_list)
                    first_result = results_list[0]
                    curr_url = extract_Url_From_Href(first_result)
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
        except:
            print(f"An exception occurred.")
            pass

    print(f"Valid Urls:")
    with open(f"{outFolder}/valid_urls.txt", "a") as f4:
        for ur in valid_urls:
            print(ur)
            f4.write(f"{ur}\n")
    
    

