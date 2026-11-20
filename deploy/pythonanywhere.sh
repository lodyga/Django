#!/bin/bash
set -e

PROJECT_DIR="/home/ukasz/codesite"

source "$PROJECT_DIR/deploy/common.sh"

VENV="/home/ukasz/.virtualenvs/.django5env"

cd "$PROJECT_DIR"

echo "Pulling latest changes..."
deploy_code

echo "Activating virtual environment..."
source "$VENV/bin/activate"

echo "Installing dependencies..."
install_dependencies

echo "Applying migrations..."
run_migrations

echo "Collecting static files..."
collect_static

touch /var/www/ukasz_eu_pythonanywhere_com_wsgi.py

echo "Deployment completed!"
