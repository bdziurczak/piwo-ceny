#scrap data from https://www.zabka.pl/strefa-piwa/, goal is to have a list of beers with name, price for 1 unit
#price for 1 unit with discount and discount conditions
#I want to use only standard libraries

import json
from urllib.request import urlopen
from html.parser import HTMLParser

class BeerDataScraper:
    '''This class is responsible for scraping beer data from the Żabka website.'''
    def __init__(self):
        self._zabka_beer_data = None
        self._paths = None
         
    async def _pull(self):
        self._paths = await self.__get_paths()
        self._zabka_beer_data = await self.__scrape_zabka_beer_data()
        
    async def export(self):
        await self._pull()
        assert self._zabka_beer_data is not None, "zabka_beer_data is not populated"
        return self._zabka_beer_data
        
    async def export_to_json(self, path):
        await self._pull()
        assert self._zabka_beer_data is not None, "zabka_beer_data is not populated"
        return json.dumps(self._zabka_beer_data,indent=4, ensure_ascii=False)
            
    @staticmethod
    async def __get_paths():
        with open("paths.json", "r", encoding="utf-8") as f:
            paths = json.load(f)
            return paths


    async def __scrape_zabka_beer_data(self):
        assert self._paths is not None
        zabka_html_path = self._paths["local"]["zabka_html_file"]
        with open(zabka_html_path, "w+", encoding="utf-8") as zabka_html_file:
            html_content = zabka_html_file.read()
            if not html_content:
                url = self._paths["web"]["zabka_url"]
                html_content = urlopen(url).read().decode('utf8')
                zabka_html_file.write(html_content)
            parser = self.__Scraper(zabka_html_path)
            parser.feed(html_content)
            
            return parser.data
        
    class __Scraper(HTMLParser):
        """This Parser scraps data about beverages from Żabka website.
        There's assumption that beverage data are ordered in HTML the same way for every beer
        If for example website will change and order of features will change, then this parser should also be modified"""

        def __init__(self, zabka_html_path=None):
            super().__init__()
            self.ZABKA_HTML_PATH = zabka_html_path
            self.read_mode = False
            self.data = []
            self.data_record_buff = {}
            self.class_buff = ""
            self.interesting_classes = ("product-item-content__title",
                                        "product-item-content__text product-item-content__informations",
                                        "product-label__text", "product-info__bottom-label")
            #dictionary to translate from css classes to data fields
            # this is not a good solution, but it works for now
            self.fancy_classes = {
                "product-item-content__title": "name",
                "product-item-content__text product-item-content__informations": "price",
                "product-label__text": "terms",
                "product-info__bottom-label": "cut price"
            }
        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            if "class" in attrs_dict:
                contained_interesting_classes = []
                for e in self.interesting_classes:
                    if e in attrs_dict["class"]:
                        contained_interesting_classes.append(e)
                self.read_mode = True
                self.class_buff = ' '.join(contained_interesting_classes)

                if contained_interesting_classes:
                    #distinguishing different beers by a div with title
                    if "product-item-content__title" in attrs_dict["class"]:
                        self.data.append(self.data_record_buff) if self.data_record_buff else None
                        self.data_record_buff = {} #clearing buffer
                else:
                    self.read_mode = False

        def handle_data(self, data):
            if self.read_mode:
                tdata = data.strip()
                if tdata:
                    self.data_record_buff[self.fancy_classes[self.class_buff]] = tdata #avoid adding strings only with whitespaces
            pass

        def handle_endtag(self, tag):
            if tag == "br":
                self.read_mode = True
            pass