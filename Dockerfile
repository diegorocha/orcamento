FROM python:3.6-alpine

RUN apk add gcc musl-dev python3-dev postgresql-dev

RUN apk add libxslt-dev

RUN pip install pip==21.0.1

WORKDIR /usr/app

COPY requirements.txt /usr/app

RUN pip install -r /usr/app/requirements.txt

COPY . /usr/app

EXPOSE 80

ENTRYPOINT ["gunicorn", "-b", ":80", "core.wsgi"]
