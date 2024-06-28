#!/bin/bash
# Test the substitute command using non-slash delimiters

output=$(echo "fishing" | python3 eddy.py 's@i@o@g')
expected_output="foshong"

if [[ "$output" == "$expected_output" ]]; then
  echo "Test Passed: Substitute command with non-slash delimiter works as expected."
  exit 0
else
  echo "Test Failed: Substitute command with non-slash delimiter did not work as expected."
  exit 1
fi

