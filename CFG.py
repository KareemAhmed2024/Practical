import nltk
from nltk import CFG
from nltk.parse import ChartParser

# Define the CFG grammar
grammar = CFG.fromstring("""
  S -> S '+' S | S '*' S | '(' S ')' | 'a'
""")

# The input string to be checked for ambiguity
input_string = "a+a*a"

# Tokenize the string based on whitespace
tokens = list(input_string)  # ['a', '+', 'a', '*', 'a']

# Create a parser for the grammar
parser = ChartParser(grammar)

# Parse the tokens to get all possible parse trees
trees = list(parser.parse(tokens))

# Check if there is more than one parse tree
if len(trees) > 1:
    print(f"The grammar is ambiguous for the string '{input_string}' — {len(trees)} parse trees found.")
    for i, tree in enumerate(trees, 1):
        print(f"\nParse Tree #{i}:")
        print(tree)
        tree.pretty_print()
else:
    print(f"The grammar is unambiguous for the string '{input_string}' — only one parse tree found.")
