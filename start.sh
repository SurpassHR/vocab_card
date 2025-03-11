#!/bin/bash

# 启动后端
uvicorn server:app --reload &

# 启动前端
cd review-words-frontend && npm start