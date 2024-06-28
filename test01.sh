#!/bin/bash
# Test the print command on a sequence of numbers

output=$(seq 1 5 | python3 eddy.py '2p')
expected_output="1
2
2
3
4
5"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Print command works as expected."
  exit 0
else
  echo "Test Failed: Print command did not work as expected."
  exit 1
fi

