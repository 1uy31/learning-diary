FROM python:3.10.0-slim

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    libpq-dev \
    build-essential


COPY pyproject.toml /app/

RUN pip install --upgrade pip \
    && pip install poetry && poetry config virtualenvs.create false && poetry install

ADD . /app/

EXPOSE 5000
