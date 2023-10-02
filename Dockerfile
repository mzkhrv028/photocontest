FROM python:3.10-slim

LABEL maintainer="mzakharov028@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]