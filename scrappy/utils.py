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

    shift = 3
    return title_list[shift:shift + num_titles]

def searchify_news_title(news_title):
    char_replacements = [("%", "%25"), ("'", "%27"), (":", "%3A"), ("$", "%24"), ("#", "%23"), (",", '%2C')]

    for replacements in char_replacements:
        news_title = news_title.replace(replacements[0], replacements[1])

    return news_title

def format_query(search_string):
    prefix = 'https://www.bing.com/search?q="'
    suffix = '"+news&filters=ex1%3a"ez5_18180_18223"&form=QBRE&'
    return prefix + search_string + suffix

def cls():
    import os
    os.system('clear')