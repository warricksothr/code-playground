# Permutations

## Usage

```bash
usage: permutations.py [-h] [--itertools] file

An application that consumes a file with one or more lines. Each line will be evaluated for all permutations of the provided
characters and the resulting permutations will be printed in alphabetical order.

positional arguments:
  file         the path to a file with one or more lines

options:
  -h, --help   show this help message and exit
  --itertools  Use itertools for permutation calculations
````

## Examples

sample.txt
```
hat
abc
Zu6
T
```

Process the file by providing the path to the file
```bash
$ ./permutations.py sample.txt
aht,ath,hat,hta,tah,tha
abc,acb,bac,bca,cab,cba
6Zu,6uZ,Z6u,Zu6,u6Z,uZ6
T
AA
```