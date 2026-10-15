#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 01: AI Hardware Portability & OpenShift AI Benchmarking"
echo "========================================================================"
cd "$(dirname "$0")"
python3 benchmark_portability.py
echo "[✔] Lab 01 Completed Successfully."
