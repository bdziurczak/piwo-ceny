from fastapi import FastAPI
import json 
from fastapi.responses import JSONResponse
from beer_data_scraper import BeerDataScraper
from fastapi.responses import RedirectResponse
import re

async def get_beer_data():
    beer_data = BeerDataScraper()
    return await beer_data.export()


app = FastAPI()

app.add_api_route("/", lambda: RedirectResponse(url="/all-beers"), methods=["GET"])


@app.get("/all-beers")
async def read_root():
    beers_on_discount = await get_beer_data()
    return JSONResponse(content=beers_on_discount)


@app.get("/cheapest-beer")
async def get_cheapest_beer():
    beers_on_discount = await get_beer_data()
    if not beers_on_discount:
        return JSONResponse(content={"error": "No beers found"}, status_code=404)
    
    def get_beer_score(price, terms):  
        price = float(price.replace("zł", "").replace(",", ".").replace("od", " ").strip())
        try:
            number_of_beers = int(re.findall(r'\d+', terms)[0])  # only number in terms is a number of beers
        except (IndexError, ValueError):
            number_of_beers = 1
        return price / number_of_beers if number_of_beers else float(100)  # Avoid division by zero  
    scores = [(x,get_beer_score(x["cut price"], x["terms"])) for x in beers_on_discount if "cut price" in x and "terms" in x]
    cheapest_beer = min(scores, key=lambda x: x[1], default=None)
    return JSONResponse(content=cheapest_beer[0])