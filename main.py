import os
import sys
from lark import Lark
from pathlib import Path

# ANSI color codes for terminal output
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

# Check if --noerr flag is provided
show_errors = "--noerr" not in sys.argv

# Read the grammar file
grammar = Path('grammar.lark').read_text()

# Try to create the parser
try:
    parser = Lark(grammar)
except Exception as e:
    if show_errors:
        print(f"Error creating parser: {str(e)}")
    parser = None

# Get all files in the problems directory
problem_files = os.listdir('problems')

# Try parsing each file
for filename in problem_files:
    if filename.endswith('.chem'):
        file_path = os.path.join('problems', filename)
        try:
            # Read the file content
            content = Path(file_path).read_text()
            
            # Try to parse the content if parser was created successfully
            if parser:
                parser.parse(content)
                print(f"{GREEN}PASS: {filename}{RESET}")
            else:
                # If parser creation failed, we can't parse
                print(f"{RED}FAIL: {filename}{RESET}")
        except Exception as e:
            # If an exception was raised, parsing failed
            print(f"{RED}FAIL: {filename}{RESET}")
            if show_errors:
                print(f"  Error: {str(e)}")
