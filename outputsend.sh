#!/bin/bash

PROJECT=`basename \`dirname $0\``
OUTPUTFILE=/usr/local/orbit/$PROJECT/data/output

if [ -f $OUTPUTFILE ]
then
	cat $OUTPUTFILE
	rm $OUTPUTFILE
fi
