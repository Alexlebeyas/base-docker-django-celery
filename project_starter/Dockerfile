FROM python:3.5-alpine
COPY . /PROJECT_NAME
WORKDIR /PROJECT_NAME
COPY pip.conf /root/.pip/pip.conf
RUN apk update && apk add build-base postgresql-dev gettext-dev # jpeg-dev zlib-dev uncomment this for Pillow package
RUN pip install -r requirements.txt
