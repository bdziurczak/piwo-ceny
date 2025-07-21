from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from scraping.scraper import Scraper

app = FastAPI()

app.add_api_route("/", lambda: RedirectResponse(url="/all-beers"), methods=["GET"])


@app.get("/all-beers")
async def read_root():
    beers_on_discount = await Scraper().get_beer_data()
    return beers_on_discount