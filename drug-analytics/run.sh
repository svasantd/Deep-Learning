#!/bin/bash

# Startup script for Drug Analytics Workbench

echo "═══════════════════════════════════════════════════════"
echo "  💊 SPECIALTY DRUG PORTFOLIO ANALYTICS WORKBENCH"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Starting application..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Run the app
streamlit run app.py --server.port 8501 --server.address localhost

echo ""
echo "Application stopped."
