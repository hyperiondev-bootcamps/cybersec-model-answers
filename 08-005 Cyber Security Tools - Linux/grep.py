#!/usr/bin/python3

"""
This script searches for a specified string (needle) within lines of input
and prints those lines where the needle is found.

Usage:
    - To search from standard input:
      python script.py needle

    - To search within a file:
      python script.py needle filename

In both cases, 'needle' is the string to search for. If reading from a file,
the script will read the file's content line by line.

Modules:
    sys: Provides access to command-line arguments and standard input/output
    streams.
"""

import sys


def match(source, needle):
    """
    Searches for a specified 'needle' string within a list of 'source' strings.

    Args:
        source (iterable): An iterable of strings to be searched.
        needle (str): The string to search for within each string in 'source'.

    Prints:
        The lines from 'source' that contain 'needle'.

    Example:
        If 'source' is ['line1', 'needle line2', 'line3'] and 'needle' is 
        'needle', the function will print 'needle line2'.
    """
    for haystack in source:
        # Check if 'needle' is found in 'haystack'.
        # If found, print the 'haystack' string.
        if haystack.find(needle) >= 0:
            print(haystack, end='')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Read from stdin and call 'match' with the provided needle.
        match(sys.stdin, sys.argv[1])
    elif len(sys.argv) == 3:
        # Read from the specified file and call 'match' with the provided needle.
        with open(sys.argv[2], encoding='utf-8') as file:
            lines = file.readlines()
            match(lines, sys.argv[1])
