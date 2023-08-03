# pull official base image
FROM python:3.11-slim

# set work directory
ARG WORKDIR=/usr/src/app
ARG VIRTUAL_ENV=${WORKDIR}/.venv
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

WORKDIR ${WORKDIR}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# copy requirements file
COPY pyproject.toml poetry.lock ./

# install dependencies
RUN --mount=type=cache,target=${HOME}/.cache/pypoetry \
    python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root

# copy project
COPY app app
COPY tests tests
