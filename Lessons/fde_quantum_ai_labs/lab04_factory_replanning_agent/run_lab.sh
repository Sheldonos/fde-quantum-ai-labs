#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 04: Factory Logistics Dynamic Replanning (QAOA vs Classical)"
echo "========================================================================"
cd "$(dirname "$0")"
python3 factory_replanning_bench.py
echo "[✔] Lab 04 Completed Successfully."
