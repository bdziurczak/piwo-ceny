# Data extraction, cleaning
from bs4 import BeautifulSoup
from scraper import Scraper


class Parser:
    def __init__(self):
        pass
    async def zabka_parse(self) -> list[tuple[str,str,float]]:
        """
        Asynchronously parses product information from the Żabka website.
        Fetches HTML content using the Scraper.zabka_scrape method, parses it with BeautifulSoup,
        and extracts product titles, terms, and cut prices. Returns a list of tuples, where each tuple
        contains (title, term, cut_price) for a product.
        Returns:
            list of tuples: Each tuple contains (title, term, cut_price) as strings.
        Raises:
            ValueError: If the scraper returns an empty result.
        """
        html = await Scraper.zabka_scrape()
        if not html:
            raise ValueError("Scraper returned empty result")
        
        soup = BeautifulSoup(html, 'html.parser')


        beer_items = soup.find_all("div", class_="beer-item")
        beers: list[tuple] = []
        for item in beer_items:
            title = item.find("h3", class_="product-item-content__title").text.strip()
            terms = [i.text.strip() for i in item.find_all("span", class_="product-label__text")]
            
            cut_price = item.find("span", class_="product-info__bottom-label")
            cut_price = cut_price.text.strip() if cut_price else None
            if cut_price:
                cut_price = cut_price.replace("zł", "").strip()

                #Reverse string, take part before the space(only number), reverse back and replace comma with dot
                cut_price = float(cut_price[::-1].split(' ', 1)[0][::-1].replace(',', '.'))

            beers.append((title if title else "", terms, cut_price if cut_price else ""))
        return beers


async def main():
    parser = Parser()
    beers = await parser.zabka_parse()
    print(beers)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())