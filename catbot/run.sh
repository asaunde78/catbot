#!/bin/sh
file=$1;
echo "running file: $file.py";
screen -X -S $file quit;
screen -d -m -S $file python3 $file.py; 

