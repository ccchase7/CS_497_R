import re

def extract_Url_From_Href(url_string):
    href = re.findall(r"href=\"[^ ]*\"", str(url_string))
    return href[0][6:len(href[0]) - 1]

def extract_News_Source(source_string):
    source = re.findall(r"data-author=\"[^\"]*\"", str(source_string))
    return source[0][13:len(source[0]) - 1]

def get_Mind_Titles(num_titles):
    print("Loading dataset titles...")
    import pandas as pd

    input_file = './mind/news.tsv'

    df = pd.read_csv(input_file, sep='\t')
    df.columns = ['News ID', 'Category', 'SubCategory','Title', 'Abstract', 'URL', 'Title Entities', 'Abstract Entites']

    title_list = list(df["Title"])
    print(f"{len(title_list)} titles found")

    shift = 0
    if num_titles > 0 and num_titles < len(title_list):
        return title_list[shift:shift + num_titles]
    elif num_titles < 0:
        print(f"Processing all {len(title_list)} titles")
        return title_list[shift:]

def searchify_news_title(news_title):
    char_replacements = [("%", "%25"), ("'", "%27"), (":", "%3A"), ("$", "%24"), ("#", "%23"), (",", '%2C')]

    for replacements in char_replacements:
        news_title = news_title.replace(replacements[0], replacements[1])

    return news_title

def format_query(search_string):
    prefix = 'https://www.bing.com/search?q="'
    suffix = '"+news&filters=ex1%3a"ez5_18180_18223"&form=QBRE&'
    return prefix + search_string + suffix

def curl_url_to_file(url, file_name):
    from Requests import Requester
    from bs4 import BeautifulSoup as bs

    requester = Requester()
    search_dom = requester.get_request(url)
    b = bs(search_dom.text, 'html.parser')

    with open(file_name, "w") as f2:
        f2.write(b.prettify())

def in_date_range(date_in_question):
    from dateutil import parser as dtparser

    start_date = dtparser.parse('Oct 11, 2019')
    end_date = dtparser.parse('Nov 23, 2019')
    date = dtparser.parse(date_in_question)

    return date > start_date and date < end_date

def json_to_SearchResult(json_string):
    import json
    from SearchResult import SearchResult

    return json.loads(json_string, object_hook=lambda d: SearchResult(**d))

def cls():
    import os
    os.system('clear')