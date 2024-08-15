# Dockerfile для Python програми

FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install pymongo

EXPOSE 3000
EXPOSE 5000

CMD ["python", "main.py"]
