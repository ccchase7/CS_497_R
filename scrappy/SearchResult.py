class SearchResult:
    def __init__(self, title, query_url, index_number, result_title, date, article_url) -> None:
        self.title = title
        self.query_url = query_url
        self.index_number = index_number
        self.result_title = result_title
        self.date = date
        self.article_url = article_url

    def _print(self):
        print(f"Title: {self.title}")
        print(f"Query URL: {self.query_url}")
        print(f"Index Number: {self.index_number}")
        print(f"Result Title: {self.result_title}")
        print(f"Date: {self.date}")
        print(f"URL: {self.article_url}")