FROM python:3.9

ENV APP_HOME /ic-light-api
WORKDIR $APP_HOME
COPY . .

RUN apt-get update && apt-get install
RUN apt-get install -y cmake

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 iclight:app