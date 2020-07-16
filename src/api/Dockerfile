FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi \
    && pip install --no-cache-dir pyzabbix pymongo pydantic numpy
COPY ./src/api/api /app
