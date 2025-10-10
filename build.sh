#!/bin/bash
set -e
python3 manage.py migrate
python3 manage.py populate_books
python3 manage.py createsuperuser --no-input --username admin --email chetan.chadalavada@gmail.com --pass 123
