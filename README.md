Description
===========
Cisco network devices configuration version control


Requirements
============
1) python >= 3.6

2) python module paramiko: connect to cisco devices via ssh


Installation
============
1) Clone pypmcmon repo to directory /usr/local/orbit to version control server:
```
sudo mkdir -p /usr/local/orbit
cd /usr/local/orbit
sudo git clone https://github.com/pavlovdo/pyconfigvc
```

2) A) Check execute permissions for scripts:
```
ls -l *.py *.sh
```
B) If not:
```
sudo chmod +x *.py *.sh
```

3) Give access special user confvc to cisco devices read full config;

4) Change example configuration file pyconfigvc.conf: author_name, committer_name, author_email, committer_email,
login/password for network devices, and enable password for cisco asa;

5) Change example configuration file devices.conf: type, names and ip addresses of cisco devices;

6) Further you have options: run scripts from host or run scripts from docker container.

If you want to run scripts from host:

A) Install Python 3 and pip3 if it is not installed;

B) Install required python modules:
```
pip3 install -r requirements.txt
```

C) Plan and create cron jobs for run cisco devices configuration backup and version control:
```
echo "00 04 * * *	/usr/local/orbit/pyconfigvc/pyconfigvc.py > /usr/local/orbit/pyconfigvc/data/output" > /tmp/crontab && \
crontab /tmp/crontab && rm /tmp/crontab
```

If you want to run scripts from docker container:

A) Run build.sh:
```
cd /usr/local/orbit/pyconfigvc
./build.sh
```

B) Run dockerrun.sh;
```
./dockerrun.sh
```


Notes
======
1) For send exception alarms via slack hook to your slack channel, set parameter slack_hook in conf.d/pypypmcmon.conf.
More details in https://api.slack.com/messaging/webhooks


Tested
======
Cisco 2960/2960X, 3650/3850, ASA 55xx/ASA 55xx-X, ISR 2921, Nexus 9372


Related Links
=============
http://www.paramiko.org/

https://api.slack.com/messaging/webhooks

