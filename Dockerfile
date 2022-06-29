FROM python:3.9.6-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PPYTHONENCODING utf-8

WORKDIR /usr/src/app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN ["chmod","+x","/usr/src/app/entrypoint.sh"]

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]