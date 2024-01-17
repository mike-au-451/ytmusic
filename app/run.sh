#!/bin/bash

gunicorn --reload app:app -b $(ip -4 a | awk '/inet.*eth0/{split($2, a, "/"); print a[1]}'):5678
