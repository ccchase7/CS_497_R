from Requests import Requester
from SearchResult import SearchResult
from utils import *
from bs4 import BeautifulSoup as bs
import json
from time import sleep
from scrape_utils import *

NUM_TITLES_TO_PROCESS = -1
to_file = False
outFile = "zsearch_results_output2.txt"
urlOutFile = "zsearch_valid_urls2.txt"
notFoundFile = "zsearch_query_not_found2.txt"
focusFile = "focus_queries2.txt"

requester = Requester()

#queries = ["A little snow causes a big mess, more than 100 crashes on Minnesota roads"]
#queries = ["The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War"]
#queries = get_Mind_Titles(NUM_TITLES_TO_PROCESS)
queries = get_Not_Found_Titles()
#queries = ["NFL rushing title likely to go down to the wire"]

# Concatenate all the words, and replace special characters.
# For some reason, sometimes it finds it the second time and not the first.
# If it finds it the first time, it will not continue searching.
concat_symbs = ["+", "-"]

valid_urls = []
count = 0
print(f"Searching for Articles...")



for query in queries:
    #sleep(.5)
    try:
        count += 1
        if count % 100 == 0:
            print(f"Count: {count}")
            sleep(1)

        for concat_symb in concat_symbs:
            # Put the query into https://... format
            temp_query = format_query(f"{concat_symb}".join(searchify_news_title(query).split()))
            print(temp_query)
            # Send the request
            search_dom = requester.get_request(temp_query)
            b = bs(search_dom.text, 'html.parser')

            # Get all the search results
            results_list = b.find_all("li", class_="b_algo")
            #print(results_list)
            # To stop searching when you find a valid match
            result_found = False
            focus = False

            # Evaluate search results, if any were returned
            if len(results_list) > 0:
                print(query)
                for result in results_list:
                    try:
                        search_result = bs(str(result), 'html.parser')

                        # Check that publish date is within correct range
                        date = search_result.find_all('span', class_="news_dt")
                        if not in_date_range(date[0].text):
                            #print(f"Date not in range.")
                            continue
                        
                        # Extract search result title information
                        additional_info = search_result.find_all('h2')
                        focus = True
                        result_title = bs(str(additional_info), 'html.parser').find_all('strong')
                        if len(result_title) > 0:
                            result_title = result_title[0].text.replace("...", "")
                        else:
                            print(f"No title found.")
                            continue

                        # Extract article url
                        article_url = extract_Url_From_Href(result)
                        
                        # Format result information and write to file
                        if result_title in query or query in result_title:
                            curr_result = SearchResult(query, temp_query, count + 25000, result_title, date[0].text, article_url)
                            with open(outFile, 'a') as f1, open(urlOutFile, 'a') as f2:
                                f1.write(f"{json.dumps(curr_result.__dict__)}\n")
                                f2.write(f"{article_url}\n")

                            scrape_page(curr_result)

                            result_found = True
                            focus = False
                            break # if you found a result, don't keep going through the other search results
                        else:
                            continue
                    except:
                        pass

            if result_found: # if you got a result using "-"s, don't search using "+"s
                break
            
        if not result_found:
            with open(notFoundFile, 'a') as f3:
                f3.write(f"{query}\n")
            if focus:
                with open(focusFile, 'a') as f4:
                    f4.write(f"{query}\n")

    except KeyboardInterrupt:
        print(f"Exiting at count {count}")
        exit()
    except Exception as e:
        print(f"Trouble query: {query}")
        print(f"An exception occurred: {e}")


print(f"Done searching for articles.  Check {urlOutFile} and {outFile} for results")
    
    

