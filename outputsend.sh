#!/bin/bash

readonly PROJECT=pypmcmon
readonly OUTPUTFILE=/usr/local/orbit/$PROJECT/data/output

if [ -f $OUTPUTFILE ]
then
    cat $OUTPUTFILE
    rm $OUTPUTFILE
fi