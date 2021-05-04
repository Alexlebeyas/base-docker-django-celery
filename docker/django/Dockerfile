FROM python:3.6-slim
COPY . /ocean
WORKDIR /ocean
#COPY pip.conf /root/.pip/pip.conf
RUN apt-get update -y && apt-get install libjpeg-dev libproj-dev gettext libgettextpo-dev netcat -y
RUN pip install pip==9.0.3
RUN pip install -r requirements.txt
