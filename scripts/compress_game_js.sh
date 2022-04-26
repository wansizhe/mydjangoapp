#! /bin/bash

JS_PATH=/home/django/mydjangoapp/game/static/js
JS_PATH_DST=${JS_PATH}/dst 
JS_PATH_SRC=${JS_PATH}/src 

find $JS_PATH_SRC -type f -name '*.js' | sort | xargs cat > ${JS_PATH_DST}/game.js

echo yes | python3 manage.py collectstatic