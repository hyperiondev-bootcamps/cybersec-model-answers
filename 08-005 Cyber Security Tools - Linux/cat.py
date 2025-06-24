#!/usr/bin/python3

"""
This script processes input either from standard input (stdin) or from a
specified file.Reads lines from stdin or a file and prints them to standard
output (stdout).

Usage:
    - If no arguments are provided, reads from stdin.
    - If a filename is provided as a command-line argument, reads from that
      file.

Modules:
    sys: Provides access to command-line arguments and standard input/output
    streams.
"""
import sys


def std_in():
    """
    This is a function for reading from standard input.
    This function reads input from stdin until it is closed
    similar to the 'cat' command
    """
    for line in sys.stdin:
        print(line)


def infile(file):
    """
    This is a function for reading from a specified file
    and prints the contents of the specified file.
    GIGO (Garbage In, Garbage Out) principle applies here
    """
    try:
        with open(file, 'r', encoding='utf-8') as file_:
            content = file_.read()
            print(content)
    except FileNotFoundError:
        print(f"cat: {file}: No such file or directory")

# Determine whether to read from stdin or from a file based on
# command-line arguments.The length of sys.argv is checked to
# decide the source of input.sys.argv[0] is the name of this
# script, so we check for additional arguments (i.e., len(sys.argv) > 1).


if __name__ == "__main__":
    if len(sys.argv) > 1:
        infile(sys.argv[1])
    else:
        std_in()
