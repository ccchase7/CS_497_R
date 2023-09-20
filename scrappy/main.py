import pandas as pd

input_file = './mind/news.tsv'

df = pd.read_csv(input_file, sep='\t')
df.columns = ['News ID', 'Category', 'SubCategory','Title', 'Abstract', 'URL', 'Title Entities', 'Abstract Entites']

title_list = list(df("Title"))