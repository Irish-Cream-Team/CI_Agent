# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

# copy install file
COPY requirements.txt .

# install requirements
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","src/folder_listener.py"]