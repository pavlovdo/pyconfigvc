FROM ubuntu:latest
LABEL maintainer="Denis O. Pavlov pavlovdo@gmail.com"

ARG project

RUN apt-get update && apt-get install -y \
	cron \
	curl \
	python3 \
	python3-paramiko \
	python3-pygit2 \
	python3-requests

ENV DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

COPY *.py requirements.txt /etc/zabbix/externalscripts/${project}/
WORKDIR /etc/zabbix/externalscripts/${project}

RUN echo "00 04 * * *	/usr/local/orbit/pyconfigvc/pyconfigvc.py > /usr/local/orbit/pyconfigvc/data/output" > /tmp/crontab && \
	crontab /tmp/crontab && rm /tmp/crontab

CMD ["cron","-f"]
