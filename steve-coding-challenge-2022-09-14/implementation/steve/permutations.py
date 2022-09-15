import itertools
import sys
import pandas

# Algorithms
# Write a script which prints all the permutations of a string in alphabetical order. We consider that
# digits < upper case letters < lower case letters. The sorting should be performed in ascending
# order.
# Your program should accept a file as its first argument. The file contains input strings, one per
# line. Print to stdout the distinct permutations of the string separated by comma, in alphabetical
# order.

# Contents of sample input file:
# hat abc Zu6 T AA

# Expected output for the input above:
# aht,ath,hat,hta,tah,tha
# abc,acb,bac,bca,cab,cba
# 6Zu,6uZ,Z6u,Zu6,u6Z,uZ6
# T
# AA


def read_file():
    """Reads an input file in the program's home directory. Input file must be a .csv file
    Program returns a list of stings"""
    # Read the csv file
    file_strings = pandas.read_csv("input.csv")
    print(f"file_strings={file_strings}\n")

    # Convert the file to a dictionary to be manipulated later into a list
    file_strings = file_strings.to_dict()
    print(f"file_strings={file_strings}\n")

    # Capture whatever the file's header is
    header = (list(file_strings.keys())[0])
    print(f"header={header}\n")

    # Identify the number of string entries
    entry_count = (len(file_strings[header]))
    print(f"entry_count={entry_count}\n")
    # Merge all the entries into a single large string, adds a space after each
    text = []
    for a in range(0, entry_count):
        text.append(file_strings[header][a])
    print(f"text={text}\n")
    return text


def compile_results(input_list):
    """Takes the input list of strings, and individually runs them through the permutate function
    to get all possible combinations of rearranged characters. Returns the combinations into a new list named
    compiled_text_list. Returns the compiled_text_list.

        inputs| input_list - a list of words to be scrambled"""
    # Permutate the individual entries into the list via external function "permutate"
    compiled_text_list = []
    for i in range(0, len(input_list)):
        iteration = permutate(list_item=input_list[i])
        compiled_text_list.append(iteration)
    return compiled_text_list


def permutate(list_item):
    """Takes a string and creates all possible permutations of the individual characters rearranged. Additionally,
    it sorts the generated permuations into alphabetical order. The function also eliminates duplicate permutations.
    Example: an entry of AA or BB will only return AA or BB, not AA, AA, and BB, BB

        inputs| list_item: the item desired to be permutated"""

    characters = list(list_item)
    sorting_list = []
    # print(characters)
    for n in itertools.permutations(characters):
        # print(''.join(n))
        iteration = "".join(n)
        # print(n)
        sorting_list.append(iteration)
    sorted_list = sorted(sorting_list)

    # check for and remove any duplicates using a dictionary's built in features to only permit one replicate of a key
    # , and convert back to a list
    sorted_list = list(dict.fromkeys(sorted_list))

    # convert to a single string separated by a comma
    combined_line = ",".join(sorted_list)

    return combined_line


def output_results(final_composition):
    """Takes the list of finalized collections of permutations and exports them by stdout, one collection per line.
    This function does not return a value, only outputs data via stdout.
        inputs| final_composition - a list of lists of alphabetically sorted permutations. """

    output_dict = {}
    for z in range(0, len(final_composition)):
        output_dict[z] = final_composition[z]
        sys.stdout.write(f"{final_composition[z]}\n")


# Execution ---------

# Collect input and formate into a list
file_input = read_file()

# Generate all the permutations for each list item
composition = compile_results(input_list=file_input)

# export the final answer via stdout
output_results(final_composition=composition)
