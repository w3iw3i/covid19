FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app/data /data
COPY ./app /app

ENV PYTHONPATH /app