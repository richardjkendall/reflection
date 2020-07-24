#!/bin/sh

cd /opt/reflection
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt