#!/bin/bash

# BUGS:
# 1.  Using 10.49 in the regex is a total hack.
gunicorn \
	--daemon \
	--reload app:app \
	-b $(ip -4 a | awk '/inet.*10.49/{split($2, a, "/"); print a[1]}'):5678 \
	--access-logfile /home/mike/var/log/gunicorn/access.log
