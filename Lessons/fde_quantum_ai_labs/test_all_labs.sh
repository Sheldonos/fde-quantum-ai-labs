#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Executing Full Verification Suite: 7 IBM FDE Quantum & AI Labs"
echo "========================================================================"
cd "$(dirname "$0")"
python3 run_all_labs.py
