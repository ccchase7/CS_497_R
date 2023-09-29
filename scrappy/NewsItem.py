from SearchResult import SearchResult
import json

class NewsItem():
    def __init__(self, webpage_title, searchResult, contents) -> None:
        self.webpage_title = webpage_title
        self.searchResult = searchResult
        self.contents = contents

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)