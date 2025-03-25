import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from potapp_db import PotAppWordHistoryBD
from utils.date_utils import date_string_to_timestamp, DatePosition
from utils.config_utils import Config
from pydantic import BaseModel
import signal
import sys

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

class ComplicatedData(BaseModel):
    startDate: str
    endDate: str

@app.post("/form")
async def getComplicatedData(data: ComplicatedData):
    from utils.public_def import PROJECT_ROOT
    from os import path
    config_mgr = Config(path.join(PROJECT_ROOT, 'config.yaml'))
    db_name = config_mgr.get("database.db_name")
    table_name = config_mgr.get("database.table_name")

    pot_db = PotAppWordHistoryBD(
        db_name=db_name,
        table_name=table_name
    )

    return pot_db.procDBParse(
        startDateTimestamp=date_string_to_timestamp(
            date_str=data.startDate,
            date_position=DatePosition.LEFT_SIDE
        ),
        endDateTimestamp=date_string_to_timestamp(
            date_str=data.endDate,
            date_position=DatePosition.RIGHT_SIDE
        )
    )

if __name__ == '__main__':
    uvicorn.run(app="server:app", host="127.0.0.1", port=8000, reload=True)