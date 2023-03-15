#!/bin/sh
cd /home/asher/catbot/catbot/
screen -d -m -S basic python3 basic.py
screen -d -m -S time python3 time.py
screen -d -m -S chat python3 chat.py
screen -d -m -S league python3 league.py

