#!/bin/bash

echo "Starting CRM setup..."

write_procfile() {
    cat > Procfile <<'EOF'
web: bench serve --port 8000
socketio: node apps/frappe/socketio.js
schedule: bench schedule
worker: bench worker --queue default,short --quiet
worker_long: bench worker --queue long,default,short --quiet
EOF
}

# Check if bench already exists
if [ -f "frappe-bench/apps/frappe/frappe/__init__.py" ]; then
    echo "Bench already exists, starting..."
    cd frappe-bench
    write_procfile
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
    bench get-app crm https://github.com/auliawinda12/crm.git --branch develop

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

    # Use a minimal Procfile for containerized setup
    write_procfile

    echo "Starting bench..."
    exec bench start
fi

echo "CRM is ready at http://localhost:8000"
