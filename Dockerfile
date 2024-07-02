FROM python:3.12-alpine

RUN adduser -D app

RUN apk update && apk upgrade

RUN apk add gcc musl-dev python3-dev postgresql-dev postgresql-client libxslt-dev tzdata

USER app

ENV TZ=America/Sao_Paulo

RUN pip install pip==24.1.1

WORKDIR /usr/app

COPY requirements.txt /usr/app

RUN pip install -r /usr/app/requirements.txt

COPY . /usr/app

EXPOSE 80

ARG VERSION_CODE=dev

ENV VERSION_CODE=$VERSION_CODE

ENTRYPOINT ["gunicorn", "-b", ":80", "core.wsgi"]
