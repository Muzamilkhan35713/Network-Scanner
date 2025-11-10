#!/bin/bash
# Example usage script for Network Scanner

echo "=== Network Scanner Examples ==="
echo ""

echo "Example 1: Basic scan of localhost"
python3 network_scanner.py 127.0.0.1 -p 22,80,443
echo ""

echo "Example 2: Ping scan (host discovery)"
python3 network_scanner.py 127.0.0.1 -t ping
echo ""

echo "Example 3: Save results to JSON"
python3 network_scanner.py 127.0.0.1 -p 80,443 -o scan_results.json
echo ""

echo "Example 4: Save results to TXT"
python3 network_scanner.py 127.0.0.1 -p 22,80 -o scan_results.txt -f txt
echo ""

echo "=== Examples complete ==="
