#!/bin/bash
# Runs inside the container after the agent finishes. Tests are copied in only now.
pip install --quiet --break-system-packages pytest==8.4.1 || pip install --quiet pytest==8.4.1
python3 -m pytest "$TEST_DIR/test_outputs.py" -rA
