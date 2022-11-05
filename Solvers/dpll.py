from collections import deque
import os
import time
import sys


def get_pure_literals(cnf):
    literals = dict()
    pure_literals = tuple()
    for clause in cnf:
        for lit in clause:
            if lit not in literals:
                literals[lit] = 1
            else:
                literals[lit] += 1
    for lit in literals:
        if literals[lit] == 1:
            pure_literals += (lit,)
    return pure_literals


def remove_pure_literal_clause(pure_literal, cnf):
    for lit in pure_literal:
        for clause in cnf:
            if lit in clause:
                cnf.remove(clause)
    return cnf


def remove_unit_clause(cnf):
    for clause in cnf:
        if len(clause) == 1:
            cnf.remove(clause)
    return cnf
