import asyncio
from beer_data import BeerData

async def main():
    data = BeerData()
    await data.pull() #populate BeerData instance
    print(data.zabka_beer_data)
if __name__ == '__main__':
    asyncio.run(main())
    #a
