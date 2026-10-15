#!/usr/bin/env bash
set -e
echo "========================================================================"
echo " Running Lab 02: Quantum Job Operations Assistant & FinOps Governor"
echo "========================================================================"
cd "$(dirname "$0")"
python3 quantum_ops_agent.py
echo "[✔] Lab 02 Completed Successfully."
