FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ecommerce_api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .
