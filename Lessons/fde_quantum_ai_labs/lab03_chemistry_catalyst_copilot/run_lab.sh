#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 03: Chemistry & Battery Catalyst Copilot (SQD & VQE)"
echo "========================================================================"
cd "$(dirname "$0")"
python3 chemistry_copilot_sqd.py
echo "[✔] Lab 03 Completed Successfully."
