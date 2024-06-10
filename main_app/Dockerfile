FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask pymysql python-dotenv kafka-python

EXPOSE 5432

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5432"]
