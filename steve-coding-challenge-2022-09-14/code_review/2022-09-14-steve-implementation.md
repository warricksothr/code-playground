# Code Review - 2022-09-14

## Provided Code

<details>
  <summary>Expand To View Code</summary>

    ```python
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

        # Convert the file to a dictionary to be manipulated later into a list
        file_strings = file_strings.to_dict()

        # Capture whatever the file's header is
        header = (list(file_strings.keys())[0])

        # Identify the number of string entries
        entry_count = (len(file_strings[header]))
        # Merge all the entries into a single large string, adds a space after each
        text = []
        for a in range(0, entry_count):
            text.append(file_strings[header][a])
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
    ```
</details>

## Overview

The structure of this code is organized in a logical flow, the variables and functions are readable, the code is documented, and most importantly the code executes and produces the desired output.

### Pros:

#### The Code Is Broken Down Into Logical Tasks

1. read_file
1. compile_results
1. output_results

This destructuring of a task into subtasks is a vital part of programming for any system that will grow and change over time.

#### Nice Use Of DocStrings

```python
def permutate(list_item):
    """Takes a string and creates all possible permutations of the individual characters rearranged. Additionally,
    it sorts the generated permuations into alphabetical order. The function also eliminates duplicate permutations.
    Example: an entry of AA or BB will only return AA or BB, not AA, AA, and BB, BB
        inputs| list_item: the item desired to be permutated"""
```

I would recommend prettifying them a bit and limiting the individual line length to <90 characters for readability in terminals. <73 is the "standard" but <90 is more ergonomic. Also the PEP8 style guide has recommendations for Documentation Strings https://peps.python.org/pep-0008/#documentation-strings.

```python
def permutate(list_item):
    """Generate the permutations for the provided list

    Takes a string and creates all possible permutations of the individual characters
    rearranged. Additionally, it sorts the generated permuations into alphabetical
    order. The function also eliminates duplicate permutations.
    
    Example: an entry of AA or BB will only return AA or BB, not AA, AA, and BB, BB

    Arguments:
    list_item -- the item desired to be permutated
    """
```

#### The Code Is Documented

Complex or confusing code is at least partially documented and this helps the readability

### Cons:

#### The Code Fails Some Of The Stated Requirements

- Your program should accept a file as its first argument

The code above does not read an argument to determine the path to the input file. An example implementation of this can be as simple as 

```python
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
```

Or more ergonomically

```python

```

- The code imposes an additional restriction of only accepting a CSV file

This new requirement partially violates the requirement 

> The file contains input strings, one per line

by imposing the csv format restrictions on top of the requirement. In particular you needed to handle CSV headers because of this additional restriction.

#### The Code Is Missing the Conventional Entrypoint For Python Scripts

This documentation (https://docs.python.org/3/library/__main__.html#idiomatic-usage) describes the functionality of this entrypoint as a standardization for executable python scripts. It also documents why this functionality is desired and standardized.

#### Iteration And Collection Is Not Quite Pythonic

```python
characters = list(list_item)
sorting_list = []
# print(characters)
for n in itertools.permutations(characters):
    # print(''.join(n))
    iteration = "".join(n)
    # print(n)
    sorting_list.append(iteration)
sorted_list = sorted(sorting_list)
```

this could be rewritten as

```python
sorted_list = sorted(["".join(iteration) for iteration in itertools.permutations(list(list_item))])
```

Which requires less allocations and avoids declaring an empty list and appending to it.

An alternative version can get us the removal of duplicates for free by using a set comprehension (https://docs.python.org/3/tutorial/datastructures.html#sets)

```python
sorted_list = sorted({"".join(iteration) for iteration in itertools.permutations(list(list_item))})
```

Comprehensions are pretty central to python and because of how python optimizes itself a list comprehension will often be faster than allocating a list and adding to it repeatedly. https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Loops

More efficient generator comprehensions can also be leverged to do the work during invocation instead of at declaration.

Can you convert this

```python
compiled_text_list = []
for i in range(0, len(input_list)):
    iteration = permutate(list_item=input_list[i])
    compiled_text_list.append(iteration)
return compiled_text_list
```

using knowledge of collection comprehensions into something more pythonic?

#### Writing For Loops Using Indexes Is Odd For Python

In other languages it can be normal to iterate over a collection using an index by performing positional lookups. In python this is considered `ugly` code and as such not very pythonic.

```python
text = []
for a in range(0, entry_count):
    text.append(file_strings[header][a])
```

can instead be written as

```python
for a in file_strings[header]:
    text.append(a)
```

or with a comprehension

```
text = [a for a in file_strings[header]]
```

when you need to access the index of a collection the builtin `enumerate` function will save you from the boilerplate to check the bounds of the collection you're selecting from.

```python
for index, a in enumerate(file_strings[heder]):
    print(f"value at index {index} of file_strings == {a}")
```

#### Writing To Stdout Directly Is Odd

I know why this confusion happened, but I hope to communicate the why code like this is considered a `smell`

```python
sys.stdout.write(f"{final_composition[z]}\n")
```

The direct use of sys.stdout (https://docs.python.org/3/library/sys.html#sys.stdout) is unconventional because these are essentially file descriptors and sys.stdout behaves differently depending on whether the python interpreter thinks its inside an interactive session or not. Writing to these buffers `raw` can be very powerful, but is often not `pythonic` and comes with additional concerns. Seeing code like this I would ask why this method of writing to stdout was chosen and would expect rationalle that took the above into account or pointed out bad requirements leading to this confusion. This question would be magnified because I saw the use of `print()` functions for debugging in the provided code.

#### 

Additional dictionaries are created but never used

```python
output_dict = {}
for z in range(0, len(final_composition)):
    output_dict[z] = final_composition[z]
    sys.stdout.write(f"{final_composition[z]}\n")
```

In the above code you create and populate an output dictionary but you never read the output_dictionary or return it. This allocation that does nothing is a code smell and can be cleaned up.

#### The Code Is Missing An Algorithm Implementation

I waffled on calling this a con since the requirements don't call out not using a library for the actual permutation work. But I feel that a coding test like this is also looking to talk about algorithm complexity and your comfort of describing the performance characteristics of code.

### Code Style

Using a tool like [Black](https://github.com/psf/black) will help format your code in a standard way to share with other developers 

#### Order Imports

These imports should be ordered alphabetically and follow the guidelines for imports defined in [PEP8](https://peps.python.org/pep-0008/#imports)
```python
import itertools
import sys
import pandas
```

#### Single Letter Internal Iteration Values Are Less Than Ideal

Python is an easy to read language and encourages writing readable code over clever code. This is often ignored for small tight loops with good documentation or very clear surrounding code. Remember your code will be read orders of magnitude more times than it will be edited. Short variable names only save typing time and come at the cost of readability and clarity.

```python
for n in itertools.permutations(characters):
    # print(''.join(n))
    iteration = "".join(n)
    # print(n)
    sorting_list.append(iteration)
```

would be more immediately readable as 

```python
for permutation in itertools.permutations(characters):
    # itertools.permutations returns a list of tuples, so each tuple needs to be 
    # joined to produce the desired output.
    iteration = "".join(permutation)
    sorting_list.append(iteration)
```

and quite possibly even more readable as

```python
for permutation_parts in itertools.permutations(characters):
    permutation = "".join(permutation_parts)
    sorting_list.append(permutation)
```

#### Remove Commented Out Debugging Code

Debugging code should be removed from code being submitted for evaluation. If debugging was deeply invloved in the task, it should use the available standard library tools for logging or debugging and be placed behind a flag.

```python
# print(characters)
```

AND

```python
# print(''.join(n))
```

AND

```python
# print(n)
```

Example of debugging that might be okay to leave in code

Python standard library logging tooling - https://docs.python.org/3/library/logging.html

```python
log.debug("permutations of %s == %s", x, permutations_of_x)
```

OR

Python standard library debugging tooling - https://peps.python.org/pep-0553/

```python
# assuming that `debugging` is some sort of runtime variable that allows you to enable/disable the debugging functionality
if debugging:
    print("Entering debugging breakpoint")
    breakpoint()
```

#### Don't Over Document Code

Here are a couple of examples of code that doesn't need the documenation above it because the code iteself describes the behavior. Strive to write self documentating code so that you don't have to write complex and quickly outdated inline documentation.

```python
# Read the csv file
file_strings = pandas.read_csv("input.csv")
```

```python
# convert to a single string separated by a comma
combined_line = ",".join(sorted_list)
```

```python
# Generate all the permutations for each list item
composition = compile_results(input_list=file_input)
```