FROM python:3.7-slim

WORKDIR /backend

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y libcairo2-dev libgirepository1.0-dev \
    && pip3 install --upgrade pip \
    && pip3 install pycairo \
    && pip3 install -r requirements.txt --no-cache-dir

COPY . .

LABEL project='backend' version=1.0

CMD ["python3", "manage.py", "runserver", "0:8000"]