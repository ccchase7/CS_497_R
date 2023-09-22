from Requests import Requester
from Parses import Parser
from utils import *
from time import sleep

NUM_TITLES_TO_PROCESS = 200
OUT_QUERIES_FILE = "all_queries.txt"
OUT_VALID_QUERIES_FILE = "valid_queries.txt"

requester = Requester()

dom_path_dict = {"YAHOO!News": ["div:caas-body", "p"], "Yahoo": ["div:caas-body", "p"], "MSN": ["article"]}

#queries = ["A little snow causes a big mess, more than 100 crashes on Minnesota roads", "The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
#queries = ["The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)

# Concatenate all the words, and replace special characters.
queries = ("-".join(searchify_news_title(i).split()) for i in queries)

valid_urls = []
count = 0
for query in queries:
    try:
        count += 1
        if count % 10 == 0:
            print(f"Count: {count}")
        query = format_query(query)
        # Send the search request to the news site
        #print(f"\nSending request: {query}")
        search_dom = requester.get_request(query)
        parser = Parser(search_dom.text)
        #results_list = parser.trail_find(["body", "div", "ol"])
        results_list = parser.trail_find(["li:b_algo", "h2", "a"])

        # Extract the url and news source from the first search result
        if len(results_list) > 0:
            first_result = results_list[0]
            curr_url = extract_Url_From_Href(first_result)
            #print(f"URL: {curr_url}")
            valid_urls.append(curr_url)
            #curr_news_source = extract_News_Source(first_result)
        else:
            pass
            #print(f"No results were found.")

        #sleep(.1)
    except KeyboardInterrupt:
        exit()
    except:
        pass

print(f"Valid Urls:")
for ur in valid_urls:
    print(ur)
    
    

