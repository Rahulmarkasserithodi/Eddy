#!/bin/bash
# Test multiple operations including delete and substitute

output=$(seq 1 5 | python3 eddy.py '1d;s/2/Two/;3p')
expected_output="Two
3
4
5"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Sequence of delete and substitute commands works as expected."
  exit 0
else
  echo "Test Failed: Sequence of delete and substitute commands did not work as expected."
  exit 1
fi

