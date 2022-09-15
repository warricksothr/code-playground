#!/usr/bin/env python

import argparse
import itertools

from typing import List


def get_itertools_permutations(input: str) -> List[str]:
    permutations = {
        "".join(permutation) for permutation in itertools.permutations(input)
    }
    return sorted(permutations)


def determine_permutations(characters: List[str], base_string: str = "") -> List[str]:
    """
    Recursively determine the permutations of a list of strings.

    Pass a list of single characters to generate a classical permutation. Supply a list
    of strings to permute the combinations of those strings.
    """
    if len(characters) < 1:
        return [base_string]
    else:
        return [
            base_string + permutation
            for index, character in enumerate(characters)
            for permutation in determine_permutations(
                characters[:index] + characters[index + 1 :], character
            )
        ]


def get_permutations(input: str) -> List[str]:
    characters = [char for char in input]
    return sorted({permutation for permutation in determine_permutations(characters)})


def main(file_path: str, use_itertools: bool):
    file_lines: List[str] = []

    with open(file_path, "r") as file:
        file_lines = [line.strip() for line in file.readlines() if len(line) > 0]

    for line in file_lines:
        line_permutations: List[str]
        if use_itertools:
            line_permutations = get_itertools_permutations(line)
        else:
            line_permutations = get_permutations(line)
        print(",".join(line_permutations))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
An application that consumes a file with one or more lines. Each line will be
evaluated for all permutations of the provided characters and the resulting
permutations will be printed in alphabetical order.
"""
    )
    parser.add_argument(
        "--itertools",
        dest="use_itertools",
        action="store_true",
        help="Use itertools for permutation calculations",
    )
    parser.add_argument("file", help="the path to a file with one or more lines")
    args = parser.parse_args()

    main(args.file, args.use_itertools)
