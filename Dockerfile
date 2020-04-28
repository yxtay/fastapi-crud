# pull official base image
FROM python:3.6-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# copy requirements file
COPY requirements.txt requirements.txt

# install dependencies
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY app app
COPY tests tests

CMD uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
