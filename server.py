from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from potapp_db import PotAppWordHistoryBD
from utils import date_string_to_timestamp

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
    pot_db = PotAppWordHistoryBD(db_name='history.db', table_name='history')
    return pot_db.procDBParse(timestamp)
