from Requests import Requester
from Parses import Parser
from utils import *

NUM_TITLES_TO_PROCESS = 50

requester = Requester()

dom_path_dict = {"YAHOO!News": ["div:caas-body", "p"], "Yahoo": ["div:caas-body", "p"]}

queries = ["Fossil discovery reveals ancient koala relatives the size of small cats roamed Australia",
           "Shiny vs. Dull Side of Foil: Which Should You Use?"]#, "Ancient Supervolcano in US May Hide Largest Lithium Deposit Ever Found"]

queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)

queries = ["-".join(i.split()) for i in queries]
 
URL = ['https://www.bing.com/news/search?q=']

for url in URL:
    for query in queries:
        # Send the search request to the news site
        print(f"\nSending request: {url}{query}")
        search_dom = requester.get_request(url + query)
        parser = Parser(search_dom.text)
        results_list = parser.trail_find(["div:news-card", "a:title"])

        # Extract the url and news source from the first search result
        first_result = results_list[0]
        curr_url = extract_Url_From_Href(first_result)
        curr_news_source = extract_News_Source(first_result)
        
        print(f"URL: {curr_url}")
        print(f"News Source: {curr_news_source}")
        print(f"******************************************************************\n")

        
        if "yahoo" in curr_news_source.lower():
            curr_news_source = "Yahoo"
            print(f"Sending request:  {curr_url}")
            article_dom = requester.get_request(curr_url)
            parser = Parser(article_dom.text)
            article_content = parser.trail_find(dom_path_dict[curr_news_source])

            for ln in article_content:
                print(f"{ln}\n")
            
            print("###########################################")

