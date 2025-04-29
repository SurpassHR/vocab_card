import sys
import signal
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from potapp_db import PotAppWordHistoryBD
from pydantic import BaseModel
from utils.date_utils import dateStringToTimestamp, DatePosition
from utils.config_utils import Config
from utils.logger import Logger
from utils.public_def import CONFIG_FILE

logger = Logger(__name__).getLogger()
app = FastAPI()

# 全局数据库连接
config_mgr = Config(CONFIG_FILE)
pot_db = PotAppWordHistoryBD(
    db_name=config_mgr.get("database.db_name"),
    table_name=config_mgr.get("database.table_name")
)

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
    logger.info(f'startDate: {data.startDate}, endDate: {data.endDate}')

    startDateTimestamp=dateStringToTimestamp(
        date_str=data.startDate,
        date_position=DatePosition.LEFT_SIDE
    )
    endDateTimestamp=dateStringToTimestamp(
        date_str=data.endDate,
        date_position=DatePosition.RIGHT_SIDE
    )
    return pot_db.procDBParse(
        startDateTimestamp=startDateTimestamp,
        endDateTimestamp=endDateTimestamp
    )

def signal_handler(sig, frame):
    logger.info('接收到信号，正在清理...')
    # 在这里添加你的清理代码，例如关闭服务器连接、保存数据等
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGILL, signal_handler)
    uvicorn.run(app=app, host="127.0.0.1", port=12345, reload=False)