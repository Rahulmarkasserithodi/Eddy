#!/bin/bash
# Test multiple commands separated by semicolons

output=$(seq 1 5 | python3 eddy.py '3q;2d')
expected_output="1
2"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Multiple commands work as expected."
  exit 0
else
  echo "Test Failed: Multiple commands did not work as expected."
  exit 1
fi

