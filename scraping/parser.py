# Data extraction, cleaning
from bs4 import BeautifulSoup
from scraper import Scraper


class Parser:
    def __init__(self):
        pass
    async def zabka_parse(self) -> list[tuple[str,str,str]]:
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

        titles = [el.get_text() for el in soup.find_all("h3", class_='product-item-content__title')]
        terms = [el.get_text() for el in soup.find_all("div", class_='product-label__text')]
        cut_prices = [el.get_text() for el in soup.find_all("span", class_='product-info__bottom-label')]
        
        return list(zip(titles, terms, cut_prices))


async def main():
    parser = Parser()
    beers = await parser.zabka_parse()
    print(beers)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())