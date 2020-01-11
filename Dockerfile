FROM python:3-alpine

RUN apk update \
      && apk add --no-cache python3-dev build-base linux-headers pcre-dev curl uwsgi \
      && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:${PATH}"

WORKDIR /usr/src/
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry version && poetry install

COPY server.py server.py

ENTRYPOINT ["poetry","run", "python","server.py"]
