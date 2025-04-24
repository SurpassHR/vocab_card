import argparse
import uvicorn
import os

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["debug", "release"], help="运行模式 (debug 或 release)")
args = parser.parse_args()

os.environ["APP_MODE"] = args.mode

if args.mode == "debug":
    uvicorn.run("server:app", reload=True)
else:
    uvicorn.run("server:app")