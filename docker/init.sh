#!/bin/bash

echo "Starting CRM setup..."

# Check if bench already exists by checking for a valid file inside
if [ -f "frappe-bench/bench/__init__.py" ]; then
    echo "Bench already exists, starting..."
    cd frappe-bench
    exec bench start
else
    echo "Cleaning up invalid bench directory if exists..."
    rm -rf frappe-bench
    echo "Creating new bench..."
    bench init --skip-redis-config-generation frappe-bench --version develop
    cd frappe-bench

    # Configure hosts
    bench set-mariadb-host mariadb
    bench set-redis-cache-host redis://redis:6379
    bench set-redis-queue-host redis://redis:6379
    bench set-redis-socketio-host redis://redis:6379

    # Get CRM app from your repository
    bench get-app crm https://github.com/auliawinda12/crm --branch develop

    # Create site
    bench new-site crm.localhost \
        --force \
        --mariadb-root-password 123 \
        --admin-password admin \
        --no-mariadb-socket

    # Install apps
    bench --site crm.localhost install-app crm

    # Set developer mode
    bench --site crm.localhost set-config developer_mode 1
    bench --site crm.localhost set-config mute_emails 0
    bench --site crm.localhost set-config server_script_enabled 1
    bench --site crm.localhost clear-cache

    # Create Procfile properly with quote handling
    cat > Procfile <<'EOF'
web: frappe serve --port 8000
worker: frappe worker --queue default --quiet
worker_long: frappe worker --queue long default --quiet
EOF

    echo "Starting bench..."
    bench start
fi

echo "CRM is ready at http://localhost:8000"
