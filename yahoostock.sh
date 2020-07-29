#!/bin/bash

count=0
runTimesInHour=6

while [ $count -lt $runTimesInHour ]
do
	wget https://finance.yahoo.com/most-active
	python hw8.py most-active.html
	echo --------------------------------------------------
	echo --------------------sleeping----------------------
	echo -----------------------for------------------------
	echo --------------------10minutes---------------------
	echo --------------------------------------------------
	sleep 600
	((count++))
done
