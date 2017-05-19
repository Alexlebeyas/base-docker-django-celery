FROM python:3.5
ADD . /PROJECT_NAME
WORKDIR /PROJECT_NAME
COPY pip.conf /root/.pip/pip.conf
RUN pip install -r requirements.txt && pip install -r private_requirements.txt
