from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from potapp_db import PotAppWordHistoryBD
from utils.date_utils import date_string_to_timestamp
from utils.config_utils import Config

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/collections/{date}")
async def getCollectionByDate(date: str):
    timestamp = date_string_to_timestamp(date)
    if timestamp is None:
        return {"error": "date type wrong"}
    config_mgr = Config("utils/config.yaml")
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")
    print(f"reading db_name: {db_name}, table_name: {table_name}")
    pot_db = PotAppWordHistoryBD(db_name=db_name, table_name=table_name)
    return pot_db.procDBParse(timestamp)
