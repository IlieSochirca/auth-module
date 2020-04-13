FROM python:3.7-alpine as base
FROM base as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /local

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg

COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt

RUN apk del build-deps

FROM base

WORKDIR /src

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

RUN apk add --no-cache \
    jpeg-dev zlib-dev \
    libmagic\
    libpq


COPY ./src /src



