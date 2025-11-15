#!/bin/bash

# Populate Demo Data for CycleX
# This script loads categories and products into Odoo

echo "=========================================="
echo "CycleX Demo Data Population"
echo "=========================================="
echo ""

# Check if Odoo is running
if ! pgrep -f "odoo-bin" > /dev/null; then
    echo "❌ Error: Odoo is not running!"
    echo "Please start Odoo first."
    exit 1
fi

echo "✓ Odoo is running"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
POPULATE_SCRIPT="$SCRIPT_DIR/populate_demo_data.py"

echo "📂 Script location: $POPULATE_SCRIPT"
echo ""

# Find Odoo installation
ODOO_BIN="/home/sabry3/edu_demo/odoo18/odoo-bin"
ODOO_CONF="/home/sabry3/edu_demo/odoo.conf"

if [ ! -f "$ODOO_BIN" ]; then
    echo "❌ Error: Odoo binary not found at $ODOO_BIN"
    exit 1
fi

if [ ! -f "$ODOO_CONF" ]; then
    echo "❌ Error: Odoo config not found at $ODOO_CONF"
    exit 1
fi

echo "✓ Found Odoo binary: $ODOO_BIN"
echo "✓ Found Odoo config: $ODOO_CONF"
echo ""

echo "🚀 Populating demo data..."
echo "----------------------------------------"

# Run the script in Odoo shell context
python3 "$ODOO_BIN" shell -c "$ODOO_CONF" -d edu_demo <<EOF
exec(open('$POPULATE_SCRIPT').read())
EOF

EXIT_CODE=$?

echo "----------------------------------------"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Demo data populated successfully!"
    echo ""
    echo "🎉 You can now:"
    echo "  • View categories at: http://localhost:8501"
    echo "  • Create orders with real products"
    echo "  • Test the complete flow"
    echo ""
else
    echo "❌ Failed to populate demo data (exit code: $EXIT_CODE)"
    echo "Check the logs above for errors"
    exit 1
fi

