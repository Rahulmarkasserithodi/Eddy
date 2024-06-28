#!/bin/bash
# Test the print command for the last line using the special address $

output=$(seq 1 5 | python3 eddy.py '$p')
expected_output="1
2
3
4
5
5"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Print command for last line works as expected."
  exit 0
else
  echo "Test Failed: Print command for last line did not work as expected."
  exit 1
fi

