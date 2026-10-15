#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 05: Portfolio Scenario Optimization Workbench (QAOA)"
echo "========================================================================"
cd "$(dirname "$0")"
python3 portfolio_workbench.py
echo "[✔] Lab 05 Completed Successfully."
