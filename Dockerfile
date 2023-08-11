# Use the official PostGIS image as the base
# FROM postgis/postgis:14-3.3 AS postgis_base

# Use the official Python image as the second stage
FROM python:3.10

# Copy required libraries and files from the PostGIS image
# COPY --from=postgis_base /usr/local /usr/local

# RUN apt-get update && apt-get install -y build-essential binutils libproj-dev gdal-bin python3-gdal
RUN apt-get update && apt-get install -y postgis postgresql-client

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# copy project
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . /code/
