# syntax=docker/dockerfile:1

# Run docker build . -t confluent-cloud-audit-logger:1.0.0

FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "confluent-cloud-fetch-audit-logs.py" ]
