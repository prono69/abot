FROM python:3.8-slim-buster
RUN apt update && apt upgrade -y
RUN apt install git pip curl python3-pip -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN pip3 install --upgrade setuptools wheel
RUN apt-get -qq purge git && apt-get -y autoremove && apt-get -y autoclean
RUN mkdir /abot
WORKDIR /abot
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]

