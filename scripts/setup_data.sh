#!/usr/bin/env bash
# Quick setup script for fetching NBP gold prices
# Usage: ./setup_data.sh

set -e

echo "🏦 NBP Gold Price Setup"
echo "======================"

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found"
    echo ""
    echo "Installing Python dependencies..."
    pip install -r scripts/requirements.txt
    echo ""
    echo "Fetching gold price data..."
    python3 scripts/fetch_nbp_gold_prices.py -v
    echo ""
    echo "✅ Data updated successfully!"
    echo "📁 Output file: data/nbp-gold-prices.json"
else
    echo "❌ Python 3 not found"
    echo ""
    echo "Please install Python 3:"
    echo "  https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "🚀 Next steps:"
echo "  1. Start local server: npx http-server -p 8000"
echo "  2. Open browser: http://localhost:8000"
echo ""
