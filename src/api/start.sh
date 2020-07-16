#!/bin/sh
uvicorn --reload --log-level debug --port 8000 --host 0.0.0.0 start:app
