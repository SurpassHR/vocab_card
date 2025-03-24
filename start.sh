#!/bin/bash

# 启动后端
cd backend && uvicorn server:app --reload &

# 启动前端
cd electron-frontend && npm run dev:all &