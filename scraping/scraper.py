# Web scraping logic
from  bs4 import BeautifulSoup
from urllib.request import urlopen

class Scraper():  
    @classmethod
    async def zabka_scrape(self):
        zabka_url = "https://www.zabka.pl/strefa-piwa/"
        zabka_html = urlopen(zabka_url).read().decode('utf-8')
        return zabka_html

async def main():
    beer_data = await Scraper.zabka_scrape()
    print(beer_data)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
