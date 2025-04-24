#!/bin/bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install requirements.txt