FROM python:3-alpine

RUN apk update \
      && apk add --no-cache python3-dev build-base linux-headers pcre-dev curl \
      && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:${PATH}"

WORKDIR /usr/src/
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry version && poetry install

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/uwsgi","--ini", "uwsgi.ini"]
