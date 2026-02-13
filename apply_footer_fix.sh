#!/bin/bash
# Script to apply footer removal changes

echo "====================================="
echo "Applying Email Footer Removal Fix"
echo "====================================="
echo ""

cd /home/frappe/frappe-bench

echo "Step 1: Restarting Frappe container..."
docker compose restart frappe
echo "Waiting for container to be ready..."
sleep 10

echo ""
echo "Step 2: Running patch to clean existing email templates..."
bench --site crm.localhost execute "import crm.patches.remove_leave_conversation_footer_final as patch; patch.execute()"

echo ""
echo "Step 3: Clearing cache..."
bench --site crm.localhost clear-cache

echo ""
echo "====================================="
echo "Footer removal fix applied!"
echo "====================================="
echo ""
echo "The following changes have been made:"
echo "  - Updated crm/api/communication.py to remove footer from new emails"
echo "  - Added hook to clean emails before sending"
echo "  - Cleaned footer from existing email templates"
echo ""
echo "Please test by sending a new email."
echo ""
