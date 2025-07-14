API for getting beer data from zabka website
HTML parsing is done without any third party libraries

Architecture:
```
app/
├── main.py                 # Entry point
├── core/                  
│   ├── config.py           # Settings, e.g., database URL
│   └── scheduler.py        # For periodic scraping (optional)
├── scraping/               
│   ├── scraper.py          # Web scraping logic
│   └── parser.py           # Data extraction, cleaning
├── db/
│   ├── base.py             # SQLAlchemy base setup
│   ├── models.py           # SQLAlchemy models
│   └── crud.py             # DB read/write logic
├── schemas/
│   └── item.py             # Pydantic models for API
├── routers/
│   └── items.py            # routes for client API
├── services/
│   └── ingest.py           # Logic to scrape & save to DB
└── utils/
    └── logger.py           # logging setup
```