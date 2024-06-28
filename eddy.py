#!/usr/bin/env python3

import sys
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process simplified sed-like commands, supporting quit (q) and print (p) commands.")
    parser.add_argument('command', help="sed command to process, e.g., '3q', '/pattern/q', '3p', '/pattern/p'")
    parser.add_argument('-n', '--number-lines', action='store_true', help="Suppress automatic printing of lines unless specified by print commands.")
    parser.add_argument('-f', '--file', help="Read Eddy commands from a file.")
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=lambda x: open(x, 'r') if x != '-' else sys.stdin, help="Input files to process or '-' for standard input")
    args = parser.parse_args()

    # Split commands by semicolon or newline
    commands = [cmd.strip() for cmd in re.split(r';|\n', args.command) if cmd.strip()]

    try:
        for cmd in commands:
            process_command(cmd, args)
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

def process_command(command, args):
    # Check and execute the appropriate command
    if 'q' in command:
        process_quit_command(command, args)
    elif 'p' in command:
        process_print_command(command, args)
    elif 'd' in command:
        process_delete_command(command, args)
    elif 's' in command:
        process_substitute_command(command, args)
        
        
def print_error(error_msg):
    print(f"{sys.argv[0]}: {error_msg}", file=sys.stderr)

def process_quit_command(command, args):
    quit_threshold, is_regex = parse_quit_command(command)
    for file in args.files:
        try:
            if is_regex:
                process_file_regex_quit(file, quit_threshold, args)
            else:
                process_file_numeric_quit(file, quit_threshold, args)
        finally:
            if file is not sys.stdin:
                file.close()
def process_delete_command(command,args):
    if args.command == 'd':  # Generic delete command handling
        # Do nothing if just 'd' is provided, effectively deleting all input
        return
    delete_condition, is_regex = parse_delete_command(command)
    for file in args.files:
        try:
            if is_regex:
                process_file_regex_delete(file, delete_condition, args)
            else:
                process_file_numeric_delete(file, delete_condition, args)
        finally:
            if file is not sys.stdin:
                file.close()

def process_file_numeric_delete(file, delete_threshold, args):
    line_number = 1
    for line in file:
        # Skip printing the line if it matches the delete condition
        if line_number != delete_threshold:
            if not args.number_lines:
                print(line, end='')
        line_number += 1

def process_file_regex_delete(file, regex, args):
    for line in file:
        # Skip printing the line if it matches the delete regex
        if not regex.search(line):
            if not args.number_lines:
                print(line, end='')

def parse_delete_command(command):
    if command.endswith('d'):
        if command[:-1].isdigit():
            return int(command[:-1]), False
        elif command.startswith('/'):
            match = re.search(r'/([^/]+)/d$', command)
            if match:
                regex = re.compile(match.group(1))
                return regex, True
    return None, False
def apply_substitution(line, sub_pattern, replacement, global_flag):
    regex = re.compile(sub_pattern)
    if global_flag:
        # Apply the replacement globally
        return regex.sub(replacement, line)
    else:
        # Apply the replacement only once
        return regex.sub(replacement, line, count=1)

def process_substitute_command(command, args):
    sub_pattern, replacement, global_flag, sub_condition, is_regex = parse_substitute_command(command)
    regex = re.compile(sub_pattern)
    
    for file in args.files:
        line_number = 1
        for line in file:
            should_substitute = False
            if sub_condition is None:
                should_substitute = True
            elif is_regex and sub_condition.search(line):
                should_substitute = True
            elif not is_regex and sub_condition == line_number:
                should_substitute = True
            
            if should_substitute:
                if global_flag:
                    line = regex.sub(replacement, line)
                else:
                    line = regex.sub(replacement, line, count=1)
            
            if not args.number_lines:
                print(line, end='')
            line_number += 1
        if file is not sys.stdin:
            file.close()

def parse_substitute_command(command):
    # Find the delimiter right after 's'
    if 's' not in command:
        print_error("Invalid command: no substitution command found.")
        sys.exit(1)
    
    start_index = command.index('s') + 1
    if start_index >= len(command):
        print_error("Invalid substitution command format.")
        sys.exit(1)
    
    delimiter = command[start_index]
    parts = command[start_index+1:].split(delimiter)
    if len(parts) < 3:
        print_error("Invalid substitution command format.")
        sys.exit(1)
    
    sub_pattern = parts[0]
    replacement = parts[1]
    flags = parts[2] if len(parts) > 2 else ''
    
    global_flag = 'g' in flags
    sub_condition = None
    is_regex = False
    
    # Check for an address before 's'
    address_part = command[:start_index-1]
    if address_part.isdigit():
        sub_condition = int(address_part)
    elif address_part.startswith('/'):
        sub_condition = re.compile(address_part.strip('/'))
        is_regex = True

    return sub_pattern, replacement, global_flag, sub_condition, is_regex



def process_file_numeric_quit(file, quit_threshold, args):
    line_number = 1
    for line in file:
        if line_number > quit_threshold:
            break
        if not args.number_lines:
            print(line, end='')
        line_number += 1

def process_file_regex_quit(file, regex, args):
    for line in file:
        if not args.number_lines:
            print(line, end='')
        if regex.search(line):
            break

def parse_quit_command(command):
    if command.endswith('q'):
        if command[:-1].isdigit():
            return int(command[:-1]), False
        elif command.startswith('/'):
            match = re.search(r'/([^/]+)/q$', command)
            if match:
                regex = re.compile(match.group(1))
                return regex, True
    return None, False

def process_print_command(command, args):
    if args.command == 'p':  # Check if the command is just 'p'
        print_every_line_twice(args.files, args.number_lines)
        return

    # Continue with existing logic for specific patterns or line numbers
    pattern, is_regex = parse_print_command(command)
    for file in args.files:
        try:
            if is_regex:
                print_matching_lines(file, pattern, args.number_lines)
            else:
                print_numeric_lines(file, int(pattern), args.number_lines)
        finally:
            if file is not sys.stdin:
                file.close()

def print_every_line_twice(files, suppress_print):
    for file in files:
        for line in file:
            if not suppress_print:
                print(line, end='')
                print(line, end='')  # Print the line a second time


def parse_print_command(command):
    if 'p' in command:
        if command[:-1].isdigit():
            return command[:-1], False
        elif command.startswith('/'):
            match = re.search(r'/([^/]+)/p$', command)
            if match:
                regex = re.compile(match.group(1))
                return regex, True
    return None, False

def print_matching_lines(file, regex, suppress_print):
    for line in file:
        if regex.search(line):
            print(line, end='')
            if not suppress_print:
                print(line, end='')
        elif not suppress_print:
            print(line, end='')

def print_numeric_lines(file, line_number, suppress_print):
    current_line_number = 1
    for line in file:
        if current_line_number == line_number:
            print(line, end='')
            if not suppress_print:
                print(line, end='')
        elif not suppress_print:
            print(line, end='')
        current_line_number += 1

if __name__ == "__main__":
    main()              
