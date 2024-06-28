# Eddy
 `EDDY` is a Python program that implements a subset of `sed` editing commands. 
 
## Aims

This project aims to provide:
- Practice in Python programming.
- A clear and concrete understanding of `sed`'s core semantics.

## Introduction

`EDDY` is a Python program that implements a subset of `sed` editing commands. `sed` is a powerful stream editor used for parsing and transforming text, and `EDDY` focuses on a simplified subset of its commands. This project is designed to help understand the core semantics of `sed` through hands-on implementation in Python.

## Eddy Commands

### Subset 0

#### `q` - Quit Command

The `q` command causes `eddy.py` to exit. For example:

`sh`
seq 1 5 | python eddy.py '3q'
1
2
3


#### `p` - Print Command

The `p` command prints the input line. For example:

seq 1 5 | python eddy.py '2p'
1
2
2
3
4
5


#### `d` - Delete Command

The `d` command deletes the input line. For example:

seq 1 5 | python eddy.py '4d'
1
2
3
5


#### `s` - Substitute Command

The `s` command replaces the specified regex on the input line. For example:
seq 1 5 | python eddy.py 's/[15]/zzz/'
zzz
2
3
4
zzz


### Subset 0: `-n` Command Line Option

The `-n` command line option stops input lines from being printed by default. For example:

seq 1 5 | python eddy.py -n '3p'
3


### Subset 0: Addresses

All Eddy commands can optionally be preceded by an address specifying the line(s) they apply to. This address can either be a line number or a regex. For example:


seq 1 5 | python eddy.py '/1/p'
1
1
2
2
3
3
4
4
5
5


### Subset 0: Advanced Substitute Command

any non-whitespace character may be used to delimit a substitute command. For example:

seq 1 5 | python eddy.py 'sX[15]XzzzX'
zzz
2
3
4
zzz


## Running the Program

To run the program, use the following command:
```bash
python eddy.py '<command>'
Replace <command> with the desired Eddy command.

