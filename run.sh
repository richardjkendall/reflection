#!/bin/sh

cd /opt/reflection
source .env/bin/activate
DATA_STORE=/data waitress-serve --call 'reflection:create_app'