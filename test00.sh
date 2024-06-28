#!/bin/bash
# Test the quit command on a sequence of numbers

output=$(seq 1 5 | python3 eddy.py '3q')
expected_output="1
2
3"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Quit command works as expected."
  exit 0
else
  echo "Test Failed: Quit command did not work as expected."
  exit 1
fi

