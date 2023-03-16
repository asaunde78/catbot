#!/bin/sh
cd /home/asher/catbot/catbot/

for FILE in chat league time basic
do
    ./run.sh $FILE
done

