FROM dr.forum.lo/ubuntu:python3-cron
MAINTAINER Denis O. Pavlov pavlovdo@gmail.com

RUN apt-get update &&\
      apt-get upgrade -y &&\
	apt-get install python3-pygit2 -y &&\
	apt-get install python3-paramiko -y &&\
	apt-get install python3-requests -y

ADD configread.py /usr/local/orbit/pyconfigvc/configread.py
ADD devices.conf /usr/local/orbit/pyconfigvc/devices.conf
ADD pyconfigvc.conf /usr/local/orbit/pyconfigvc/pyconfigvc.conf
ADD pyconfigvc.py /usr/local/orbit/pyconfigvc/pyconfigvc.py
ADD pynetdevices.py /usr/local/orbit/pyconfigvc/pynetdevices.py
ADD pyslack.py /usr/local/orbit/pyconfigvc/pyslack.py

RUN echo "00 04 * * *	/usr/local/orbit/pyconfigvc/pyconfigvc.py > /usr/local/orbit/pyconfigvc/data/output" > /tmp/crontab
RUN crontab /tmp/crontab
RUN rm /tmp/crontab
CMD /usr/sbin/cron -f
