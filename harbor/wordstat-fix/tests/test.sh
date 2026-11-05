#!/bin/bash
# Harbor verifier: run hidden tests, write reward (1 = pass, 0 = fail).
mkdir -p /logs/verifier
pip install --quiet pytest==8.4.1

cd /app
python -m pytest /tests/test_outputs.py -rA
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
