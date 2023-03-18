#!/bin/sh
cd /home/asher/catbot/catbot/

screen -m -d -S catbot python3 manage.py
