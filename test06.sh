#!/bin/bash
# Test the delete command with a regular expression

output=$(seq 10 20 | python3 eddy.py '/1$/d')
expected_output="10
12
13
14
15
16
17
18
19
20"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Delete command with regex works as expected."
  exit 0
else
  echo "Test Failed: Delete command with regex did not work as expected."
  exit 1
fi

