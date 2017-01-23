#!/bin/bash

PROJECT=`basename $WORKSPACE`
PRODUCTION_SERVER=eye.forum.lo
PRODUCTION_DIR=/usr/local/orbit

ssh jenkins@$PRODUCTION_SERVER "sudo chown -R jenkins:jenkins $PRODUCTION_DIR"
ssh jenkins@$PRODUCTION_SERVER "[ -d $PRODUCTION_DIR/$PROJECT/data ] || mkdir -p $PRODUCTION_DIR/$PROJECT/data"
scp *.sh jenkins@$PRODUCTION_SERVER:$PRODUCTION_DIR/$PROJECT
ssh jenkins@$PRODUCTION_SERVER "chmod -v u+x $PRODUCTION_DIR/$PROJECT/*.sh"
ssh jenkins@$PRODUCTION_SERVER "docker stop `docker ps -q --filter ancestor=ubuntu:$PROJECT`"
ssh jenkins@$PRODUCTION_SERVER "docker build -t ubuntu:$PROJECT git@dev.forum.lo:it/$PROJECT.git"
ssh jenkins@$PRODUCTION_SERVER "$PRODUCTION_DIR/$PROJECT/dockerrun.sh"
ssh jenkins@$PRODUCTION_SERVER "echo '0 */1 * * *       $PRODUCTION_DIR/$PROJECT/outputsend.sh' >> /tmp/crontab"
ssh jenkins@$PRODUCTION_SERVER "crontab /tmp/crontab"
ssh jenkins@$PRODUCTION_SERVER "rm /tmp/crontab"
