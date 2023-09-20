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

    shift = 3
    return title_list[shift:shift + num_titles]