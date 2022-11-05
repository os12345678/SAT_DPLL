# Advanced-Algorithms-Assignment-3: 3SAT Problem

A simple implementation of a SAT solver using Brute Force, Davis-Putnam-Logemann-Loveland (DPLL) and CDCL algorithm.

## Usage

```bash
$ python3 main.py --method [brute | dpll | cdcl] [--file [input_file] | None]
```

## Input File Format

Dimacs CNF format

## Output

The output is a list of assignments to the variables that satisfy the formula. If the formula is unsatisfiable, the output is UNSAT.
