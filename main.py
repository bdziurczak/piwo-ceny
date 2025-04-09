from fastapi import FastAPI
import json 
from fastapi.responses import JSONResponse
from beer_data_scraper import BeerDataScraper

async def get_beer_data():
    beer_data = BeerDataScraper()
    return await beer_data.export()


app = FastAPI()


@app.get("/")
async def read_root():
    json_beer_data = await get_beer_data()
    return JSONResponse(content=json_beer_data)
