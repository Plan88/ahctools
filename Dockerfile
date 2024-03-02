FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY ./src ./src
COPY pyproject.toml ./
COPY ./in ./in

RUN apt-get -y update \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev

EXPOSE 8080

CMD ["python", "src/app.py"]
