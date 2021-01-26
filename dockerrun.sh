#!/bin/bash

readonly PROJECT=pyconfigvc
readonly CONFIG_DIR=/etc/orbit/$PROJECT
readonly PRODUCTION_DIR=/usr/local/orbit

message="\nRunning of container from image $PROJECT with name $PROJECT and mounting and $CONFIG_DIR:$CONFIG_DIR:ro and $PRODUCTION_DIR/$PROJECT/data:$PRODUCTION_DIR/$PROJECT/data"

docker run --detach --tty --name "$PROJECT" --restart=always --volume "$CONFIG_DIR":"$CONFIG_DIR":ro --volume $PRODUCTION_DIR/$PROJECT/data:$PRODUCTION_DIR/$PROJECT/data "$PROJECT"
echo -e "${message}"