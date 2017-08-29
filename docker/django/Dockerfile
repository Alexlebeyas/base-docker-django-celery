FROM python:3.5-slim
COPY . /PROJECT_NAME
WORKDIR /PROJECT_NAME
COPY pip.conf /root/.pip/pip.conf
RUN apt-get update -y && apt-get install libjpeg-dev libproj-dev gettext libgettextpo-dev netcat -y
RUN pip install -r requirements.txt
