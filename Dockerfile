FROM python:3.9-slim-buster
WORKDIR /app
RUN chmod -R 777 /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
LABEL Maintainer="Fareed"
CMD [ "python", "./main.py" ]