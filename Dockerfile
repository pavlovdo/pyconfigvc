FROM dr.forum.lo/ubuntu:python3-cron
MAINTAINER Denis O. Pavlov pavlovdo@gmail.com

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	python3-paramiko \
	python3-pygit2 \
	python3-requests

ADD *.py /usr/local/orbit/pyconfigvc/

RUN echo "00 04 * * *	/usr/local/orbit/pyconfigvc/pyconfigvc.py > /usr/local/orbit/pyconfigvc/data/output" > /tmp/crontab && \
	crontab /tmp/crontab && rm /tmp/crontab
CMD /usr/sbin/cron -f
