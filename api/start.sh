#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
exec uvicorn --reload --log-level debug --port 8000 --host 0.0.0.0 start:app