#!/bin/bash
# Test the delete command

output=$(seq 1 5 | python3 eddy.py '2d')
expected_output="1
3
4
5"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Delete command works as expected."
  exit 0
else
  echo "Test Failed: Delete command did not work as expected."
  exit 1
fi

