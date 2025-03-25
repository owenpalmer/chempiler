import os
import sys
from lark import Lark

# Define paths
PROBLEMS_DIR = "problems"
GRAMMAR_DIR = "grammar"

def load_grammar_files(grammar_names):
    """Load and combine multiple grammar files from the grammar directory."""
    combined_grammar = ""
    
    for name in grammar_names:
        # Add .lark extension if not provided
        if not name.endswith('.lark'):
            file_name = f"{name}.lark"
        else:
            file_name = name
            
        file_path = os.path.join(GRAMMAR_DIR, file_name)
        
        try:
            with open(file_path, 'r') as file:
                grammar_content = file.read()
                combined_grammar += grammar_content + "\n"
        except FileNotFoundError:
            print(f"Error: Grammar file '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading grammar file '{file_path}': {e}")
            return None
    
    return combined_grammar

def load_input_text(problem_name):
    """Load chemistry notation input from the problems directory."""
    # Add .chem extension if not provided
    if not problem_name.endswith('.chem'):
        file_name = f"{problem_name}.chem"
    else:
        file_name = problem_name
        
    file_path = os.path.join(PROBLEMS_DIR, file_name)
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Problem file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading problem file: {e}")
        return None

def parse_chemistry_problem(problem_name, grammar_names):
    """Parse a chemistry problem using the specified grammar files."""
    
    # Instead of combining all grammars, just use the main grammar file
    # and let Lark handle the imports
    main_grammar = grammar_names[0]  # Assume first argument is main grammar
    main_grammar_path = os.path.join(GRAMMAR_DIR, f"{main_grammar}.lark")
    
    try:
        # Use Lark.open with rel_to to handle imports properly
        chemistry_parser = Lark.open(
            main_grammar_path,
            rel_to=os.path.abspath(GRAMMAR_DIR),  # This is the key part
            parser='earley',
            propagate_positions=True,
            debug=True
        )
    except Exception as e:
        print(f"Error creating parser: {e}")
        return None
    
    # Load the input text
    input_text = load_input_text(problem_name)
    if input_text is None:
        return None
    
    # Parse the input
    try:
        parse_tree = chemistry_parser.parse(input_text)
        return parse_tree
    except Exception as e:
        print(f"Parsing error: {e}")
        print(f"Input was: {input_text}")
        return None

def print_usage():
    """Print usage information."""
    print("Usage: python main.py problem_name grammar_name1 [grammar_name2 ...]")
    print("  problem_name:   Name of the chemistry problem file in the 'problems' directory")
    print("  grammar_name1:  First grammar file in the 'grammar' directory (required)")
    print("  grammar_name2:  Additional grammar files (optional)")
    print("\nExample:")
    print("  (Loads problems/empirical_formula.chem, grammar/base.lark, etc.)")

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 3:
        print("Error: Insufficient arguments.")
        print_usage()
        sys.exit(1)
    
    # Get problem name and grammar names from command line arguments
    problem_name = sys.argv[1]
    grammar_names = sys.argv[2:]
    
    # Create directories if they don't exist
    os.makedirs(PROBLEMS_DIR, exist_ok=True)
    os.makedirs(GRAMMAR_DIR, exist_ok=True)
    
    print(f"Processing problem: {problem_name}")
    print(f"Using grammar files: {', '.join(grammar_names)}")
    
    # Parse the chemistry problem
    result = parse_chemistry_problem(problem_name, grammar_names)
    
    if result:
        print("\nSuccessfully parsed the chemistry problem!")
        print("\nParse Tree:")
        print(result.pretty())
    else:
        print("\nFailed to parse the chemistry problem.")
        sys.exit(1)