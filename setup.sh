#!/bin/bash

# python on Ubuntu uses a virtual environment,
# this script is a mnemonic for creating a venv

APPHOME=/home/mike/Play/2024/01/20240117_01/app

cd $APPHOME
python -m venv .
source bin/activate
pip install gunicorn flask ytmusicapi bleach
