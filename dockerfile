FROM python:3.12.1-alpine3.19

WORKDIR app
COPY app/app.py app/oauth.json .
RUN pip install gunicorn flask ytmusicapi bleach

CMD gunicorn app:app -b $(ip -4 a | awk '/inet.*eth0/{split($2, a, "/"); print a[1]}'):5678
