from sqlmodel import select, delete
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from .scraping.scraper import Scraper
from .models.beer_item import create_db_and_tables, BeerItem, SessionDep

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.add_api_route("/", lambda: RedirectResponse(url="/all-beers"), methods=["GET"])


@app.get("/all-beers", response_model=List[BeerItem])
async def get_all_beers(session: SessionDep):
    """Get all beers from the database"""
    beers = session.exec(select(BeerItem)).all()
    return beers


@app.get("/beers/{beer_id}", response_model=BeerItem)
async def get_beer_by_id(beer_id: int, session: SessionDep):
    """Get a specific beer by its ID"""
    beer = session.get(BeerItem, beer_id)
    if not beer:
        raise HTTPException(status_code=404, detail="Beer not found")
    return beer


@app.get("/refresh-beers")
async def refresh_beers(session: SessionDep):
    """Refresh beer data by scraping Żabka website and updating the database"""
    try:
        beers_on_discount = await Scraper().get_beer_data()

        session.exec(delete(BeerItem))
        session.commit()

        for beer_data in beers_on_discount:
            title, term, cut_price = beer_data
            beer = BeerItem(title=title, term=','.join(term), cut_price=cut_price)
            session.add(beer)

        session.commit()
        return {"message": f"Successfully updated {len(beers_on_discount)} beers"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
