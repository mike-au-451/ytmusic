# ytmusic

A demo ytmusicapi client.
You must provide your own `oauth.json` file.

Development requires a python virtual environment:
1.  You may need to install the python venv module first:
```
apt install python3.11-venv
```
2.  then create the virtual environment in the development directory.  You must be using either bash or csh:
```
cd $APPHOME
python3 -m venv .
source bin/activate
```

Once you have the venv, install dependencies:
```
pip install gunicorn flask ytmusicapi bleach
```

Run a development web server using python:
```
cd $APPHOME/app
# run with default address 192.168.0.74:5678
python app.py
# run with a specific ip and the default port
python app.py 1.2.3.4
# run with custom ip and port
python app.py 1.2.3.4 1234
```
