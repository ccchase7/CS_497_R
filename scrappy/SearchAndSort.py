from Requests import Requester
from SearchResult import SearchResult
from utils import *
from bs4 import BeautifulSoup as bs
import json
from time import sleep

NUM_TITLES_TO_PROCESS = 250
to_file = False
outFile = "search_results_output.txt"
urlOutFile = "valid_urls.txt"

requester = Requester()

dom_path_dict = {"YAHOO!News": ["div:caas-body", "p"], "Yahoo": ["div:caas-body", "p"], "MSN": ["article"]}

#queries = ["How to record your screen on Windows, macOS, iOS or Android"]
#queries = ["The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)

# Concatenate all the words, and replace special characters.
#queries = ("+".join(searchify_news_title(i).split()) for i in queries)
concat_symbs = ["+", "-"]

valid_urls = []
count = 0
print(f"Searching for Articles...")

with open(outFile, 'a') as f1, open(urlOutFile, 'a') as f2:

    for query in queries:
        try:
            count += 1
            if count % 1000 == 0:
                print(f"Count: {count}")

            for concat_symb in concat_symbs:
                # Put the query into https://... format
                temp_query = format_query(f"{concat_symb}".join(searchify_news_title(query).split()))

                # Send the request
                search_dom = requester.get_request(temp_query)
                b = bs(search_dom.text, 'html.parser')

                # Get all the search results
                results_list = b.find_all("li", class_="b_algo")

                # To stop searching when you find a valid match
                result_found = False

                # Evaluate search results, if any were returned
                if len(results_list) > 0:
                    for result in results_list:
                        search_result = bs(str(result), 'html.parser')

                        # Check that publish date is within correct range
                        date = search_result.find_all('span', class_="news_dt")
                        if not in_date_range(date[0].text):
                            continue
                        
                        # Extract search result title information
                        additional_info = search_result.find_all('h2')
                        result_title = bs(str(additional_info), 'html.parser').find_all('strong')
                        if len(result_title) > 0:
                            result_title = result_title[0].text.replace("...", "")
                        else:
                            continue

                        # Extract article url
                        article_url = extract_Url_From_Href(result)
                        
                        # Format result information and write to file
                        if result_title in query or query in result_title:
                            curr_result = SearchResult(query, temp_query, count, result_title, date[0].text, article_url)
                            f1.write(f"{json.dumps(curr_result.__dict__)}\n")
                            f2.write(f"{article_url}\n")

                            result_found = True
                            break # if you found a result, don't keep going through the other search results
                        else:
                            continue

                if result_found: # if you got a result using "-"s, don't search using "+"s
                    break

        except KeyboardInterrupt:
            print(f"Exiting...")
            exit()
        except Exception as e:
            print(f"An exception occurred: {e}")
    
    

