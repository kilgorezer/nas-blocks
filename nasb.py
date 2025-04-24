from sys import argv as args
from sys import exit as leave
from os import path as ospath
import re
import random

nestedlabels = []

def generate_content_label():
    """Generates a context label in the format #@$%=NASB-[10-digit random number]."""
    random_number = random.randint(0, 9999999999)  # Generates a random integer between 0 and 9999999999
    return f"#@$%=NASB-{random_number:010d}"

def blockstart(generated_label, extracted_condition):
    return (
        f"{extracted_condition} jump {generated_label}.begin\n"
        f"jump {generated_label}.end\n"
        f"{generated_label}.begin\n"
    )

def blockend(generated_label):
    return (
        f"if $%@#$#@$%@%#@$!@=NASB|=|\"\" msg\n"
        f"{generated_label}.end\n"
    )

def hconditional(line, cleaned_line, then_part):
    expanded = blockstart(nestedlabels[-1], then_part)
    print('Compiled: ' + repr(expanded))
    return expanded

def hend(line, cleaned_line, then_part):
    expanded = blockend(nestedlabels[-1])
    print('Compiled: ' + repr(expanded))
    return expanded

def hnone(line, cleaned_line, then_part):
    print('Compiled: ' + repr(line))
    return line

start = r"^(?:if|ifnot)\s+(?:([^\|\s]+)\|(?:=|<=|>=|<|>)\|(?:\w+|\d+(?:\.\d+)?|\".*?\"|true|false)|item\s+([^\|\s]+)|label\s+(#[^\|\s]+)|([^\|\s]+))\s+then$|^\s*else\s+then$"
end = r"^end$"

if len(args) < 2:
    print("Usage: python nasb.py input.nasb")
    leave(1)

input_filename = args[1]
base_name, _ = ospath.splitext(input_filename)
output_filename = base_name + ".nas"

try:
    errorflag = False
    with open(input_filename, 'r') as infile, open(output_filename, "w") as outfile:
        for line_number, line in enumerate(infile, 1):
            cleaned_line = line.strip()
            print(f"Line {line_number}: '{cleaned_line}'")

            start_match = re.fullmatch(start, cleaned_line)
            end_match = re.fullmatch(end, cleaned_line)

            if start_match:
                if cleaned_line.endswith("then"):
                    then_part = cleaned_line[:-5]
                    print(f"  Extracted: '{then_part}'")
                    nestedlabels.append(generate_content_label())
                    outfile.write(hconditional(line, cleaned_line, then_part))
            elif end_match:
                print(f"Line {line_number}: End of block - '{cleaned_line}'")
                outfile.write(hend(line, cleaned_line, 'else'))
                if len(nestedlabels) == 0:
                    errorflag = True
                nestedlabels.pop()
            else:
                print(f"Line {line_number}: No match - '{cleaned_line}'")
                outfile.write(hnone(line, cleaned_line, None))
            print('Original: ' + repr(line))
            print('Depth: ' + str(len(nestedlabels)) + "\n")
    if len(nestedlabels) > 0:
        errorflag = True
    if errorflag:
        print('ERROR COMPILING: Your script may not run incorrectly')
        print('REASON: Unmatched indents or incorrect syntax in conditional blocks.')

except FileNotFoundError:
    print(f"Error: Input file '{input_filename}' not found.")
    leave(1)
except Exception as e:
    print(f"An error occurred: {e}")
    leave(1)
