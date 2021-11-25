# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR .
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY app.py app.py
COPY utils.py utils.py

CMD ["python3", "app.py"]

