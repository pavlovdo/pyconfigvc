#!/bin/bash

PROJECT=`basename \`dirname $0\``
PRODUCTION_DIR=/usr/local/orbit
HOST_MOUNT_DIR=

if [ -f $PRODUCTION_DIR/$PROJECT/$PROJECT.docker.newimage ]
then
	PROJECTCONTAINERS=`sudo docker ps --filter ancestor=ubuntu:$PROJECT --format "table {{.ID}}" | sed '1,1d'`
	echo 'Stopping project '$PROJECT' containers:'
	sudo docker stop $PROJECTCONTAINERS
	if [ -z $HOST_MOUNT_DIR ]
	then
		echo -e '\nRunning of container from image ubuntu:'$PROJECT' with mounting '$PRODUCTION_DIR'/'$PROJECT'/data:'$PRODUCTION_DIR'/'$PROJECT'/data'
		sudo docker run -d -t -v $PRODUCTION_DIR/$PROJECT/data:$PRODUCTION_DIR/$PROJECT/data ubuntu:$PROJECT
	else
		echo -e '\nRunning of container from image ubuntu:'$PROJECT' with mounting '$PRODUCTION_DIR'/'$PROJECT'/data:'$PRODUCTION_DIR'/'$PROJECT'/data and '$HOST_MOUNT_DIR':'$HOST_MOUNT_DIR
		sudo docker run -d -t -v $PRODUCTION_DIR/$PROJECT/data:$PRODUCTION_DIR/$PROJECT/data -v $HOST_MOUNT_DIR:$HOST_MOUNT_DIR ubuntu:$PROJECT
	fi
	rm -f $PRODUCTION_DIR/$PROJECT/$PROJECT.docker.newimage
fi
