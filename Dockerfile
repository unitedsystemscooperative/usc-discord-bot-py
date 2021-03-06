# syntax=docker/dockerfile:1

FROM python:3.9-slim

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "/home/prod/.poetry/bin:$PATH"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD python usc_bot.py
