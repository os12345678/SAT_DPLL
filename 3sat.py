# input :: CNF file that gets converted to DIMACS file format.
# DIMACS is a line oriented format, consisting of 3 different basic types of lines.

#   A comment line. Any line that starts with "c" is comment line.

#   A summary line. This line contains information about the kind and size of the
#   problem within the file. A summary line starts with "p", continues with the
#   kind of the problem (in most cases "cnf"), the number of variables and the
#   number of clauses within this problem. Some DIMACS parsers expect this line
#   to be the first non-comment line, but some parsers can handle the file without
#   it.

#   A clause line. A clause line consists of space-separated numbers, ending with
#   a 0. Each non-zero number denotes a literal, with negative numbers being
#   negative literals of that variable, and 0 being the terminator of a line.

import itertools
import random
import time


def dimacs_parser(in_data):
    cnf = list()
    cnf.append(list())
    maxvar = 0

    for line in in_data:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            for tok in tokens:
                lit = int(tok)
                maxvar = max(maxvar, abs(lit))
                if lit == 0:
                    cnf.append(list())
                else:
                    cnf[-1].append(lit)

    assert len(cnf[-1]) == 0
    cnf.pop()

    return cnf


def brute_force(cnf):
    literals = set()
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])

    literals = list(literals)
    n = len(literals)
    for seq in itertools.product([True, False], repeat=n):
        a = set(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in cnf]):
            return True, a

    return False, None


def main():
    in_data = ['c horn? no',
               'c forced? no',
               'c mixed sat? no',
               'c clause length = 3',
               'c',
               'p cnf 20  91',
               '4 -18 19 0',
               '3 18 -5 0',
               '-5 -8 -15 0',
               '-20 7 -16 0']

    cnf = dimacs_parser(in_data)
    brute_force(cnf)


if __name__ == "__main__":
    main()
