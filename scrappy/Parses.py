from bs4 import BeautifulSoup as bs
# https://realpython.com/beautiful-soup-web-scraper-python/

class Parser:
    def __init__(self, dom) -> None:
        self.HTML_PARSER = 'html.parser'

        self.dom = dom
        self.soup = bs(dom, self.HTML_PARSER)

    def find(self, in_id=None):
        if in_id:
            res = self.soup.find(id=in_id)
            return res.prettify()
        return None
    
    def find_all(self, element_type, el_class=None, soop=None):
        if soop is None:
            soop = self.soup
        if el_class:
            return soop.find_all(element_type, class_=el_class)
        else:
            return soop.find_all(element_type)
    
    def trail_find(self, trail, soop=None):
        if soop is None:
            soop = [self.dom]

        for search_for in trail:
            new_soop = []
            for curr_soop in soop:
                curr_soop = bs(str(curr_soop), self.HTML_PARSER)
                if ":" in search_for:
                    el, cls = search_for.split(":")
                    new_soop += self.find_all(el, el_class=cls, soop=curr_soop)
                else:
                    new_soop += self.find_all(search_for, soop=curr_soop)

            soop = new_soop

            

        return soop

            


    

