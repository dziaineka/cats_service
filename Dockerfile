FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8

WORKDIR /app

RUN pip install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app