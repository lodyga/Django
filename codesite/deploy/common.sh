#!/bin/bash

deploy_code() {
    git pull origin master
}

install_dependencies() {
    pip install -r requirements.txt
}

run_migrations() {
    python manage.py migrate
}

collect_static() {
    python manage.py collectstatic --noinput
}
