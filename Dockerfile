# syntax=docker/dockerfile:1

FROM python:3.9-buster

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH "/home/prod/.poetry/bin:$PATH"

EXPOSE 5000

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "usc_bot.py" ]
