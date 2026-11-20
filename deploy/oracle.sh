#!/bin/bash
set -e

PROJECT_DIR="/home/ubuntu/codesite"

source "$PROJECT_DIR/deploy/common.sh"

cd "$PROJECT_DIR"

echo "Loading environment..."
set -a
source /etc/codesite.env
set +a

echo "Pulling latest changes..."
deploy_code

echo "Activating virtual environment..."
source .django5env/bin/activate

echo "Installing dependencies..."
install_dependencies

echo "Applying migrations..."
run_migrations

echo "Collecting static files..."
collect_static

echo "Restarting Gunicorn..."
sudo systemctl restart codesite

echo "Deployment completed!"
