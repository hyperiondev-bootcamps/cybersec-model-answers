#!/usr/bin/python3

"""
This script emulates a simplified version of the Unix `echo` command. It takes
command-line arguments, concatenates them into a single string separated by spaces,
and prints the result to standard output.

Usage:
    python3 script.py [arguments...]
    
    Example:
        python3 script.py Hello World Python
        Output: Hello World Python
"""

import sys

def array_to_string(arr):
    """
    Converts a list of strings into a single concatenated string with spaces
    between each element.

    Args:
        arr (list of str): A list of strings to be concatenated.

    Returns:
        str: A single string with each element of the list separated by a space.
    """
    output = ""
    for thing in arr:
        output += thing + " "
    return output

if __name__ == "__main__":
    # Remove the script name from the list of arguments
    sys.argv.pop(0)

    # Concatenate remaining arguments into a single string and print
    print(array_to_string(sys.argv))
