#!/bin/sh
file=$1;
source=$2
echo "running file: $file.py";

#screen -d -m -S $file python3 $file.py -s $source;
screen -X -S $file quit;
screen -d -m -S $file python3 $file.py -s $source;

