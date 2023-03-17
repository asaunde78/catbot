#!/bin/sh
file=$1;
echo "killing file: $file.py";
screen -X -S $file quit;
