#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 06: Quantum AI Training & FTQC Resource Estimator"
echo "========================================================================"
cd "$(dirname "$0")"
python3 ftqc_ai_training_estimator.py
echo "[✔] Lab 06 Completed Successfully."
