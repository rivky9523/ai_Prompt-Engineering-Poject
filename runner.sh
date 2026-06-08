#!/bin/bash
# runner.sh — safely run a single command passed as arguments
# Usage: docker run --rm <image> "<command>"

CMD="$@"
if [ -z "$CMD" ]; then
  echo "No command provided. Exiting."
  exit 0
fi

# run with a timeout to avoid long-running commands
echo "Running inside sandbox: $CMD"
timeout 5s bash -lc "$CMD"
EXIT_CODE=$?
if [ $EXIT_CODE -eq 124 ]; then
  echo "Command timed out (timeout 5s)"
fi
exit $EXIT_CODE
