FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh
COPY start-celery.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-celery.sh