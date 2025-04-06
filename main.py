import asyncio
from beer_data import BeerData

async def main():
    beer_data = BeerData()
    await beer_data.pull() #populate BeerData instance
    print(beer_data.zabka_beer_data[1])
    await beer_data.export_to_json() #export to json file
if __name__ == '__main__':
    asyncio.run(main())
    
