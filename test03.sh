#!/bin/bash
# Test the substitute command

output=$(echo "hello there" | python3 eddy.py 's/e/E/g')
expected_output="hEllo thErE"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Substitute command works as expected."
  exit 0
else
  echo "Test Failed: Substitute command did not work as expected."
  exit 1
fi

