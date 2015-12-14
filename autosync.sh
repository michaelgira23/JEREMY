#!/bin/sh

while true
do
    git pull
    git config --global --unset https.proxy
    sleep 60
done
