FROM python:3.5
ADD . /planned_parenthood
WORKDIR /planned_parenthood
COPY pip.conf /root/.pip/pip.conf
RUN pip install -r requirements.txt && pip install -r private_requirements.txt
