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
    print(data)
    from utils.public_def import CONFIG_FILE
    config_mgr = Config(CONFIG_FILE)
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

def signal_handler(sig, frame):
    print('接收到信号，正在清理...')
    # 在这里添加你的清理代码，例如关闭服务器连接、保存数据等
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGILL, signal_handler)
    uvicorn.run(app=app, host="127.0.0.1", port=8000, reload=False)