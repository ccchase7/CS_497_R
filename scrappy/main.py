from utils import *
from Requests import Requester
from Parses import Parser
from bs4 import BeautifulSoup as bs

requester = Requester()
url = 'https://golfweek.usatoday.com/2019/10/27/golf-twitter-reacts-tiger-woods-82nd-victory/'
temp_query = format_query(url)
print(f"{temp_query}")
search_dom = requester.get_request(temp_query)
b = bs(search_dom.text, 'html.parser')
results_list = b.find_all('p')

print(b)

for p in results_list:
    if p.string:
        print(p.string)