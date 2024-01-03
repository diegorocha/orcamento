FROM python:3.8-alpine

RUN apk update && apk upgrade

RUN apk add gcc musl-dev python3-dev postgresql-dev postgresql-client libxslt-dev tzdata

ENV TZ=America/Sao_Paulo

RUN pip install pip==21.1.1

WORKDIR /usr/app

COPY requirements.txt /usr/app

RUN pip install -r /usr/app/requirements.txt

COPY . /usr/app

EXPOSE 80

ARG VERSION_CODE=dev

ENV VERSION_CODE=$VERSION_CODE

ENTRYPOINT ["gunicorn", "-b", ":80", "core.wsgi"]
