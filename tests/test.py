from pysat.formula import CNF
from pysat.solvers import Solver
import pytest


def test_result(cnf):
    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            return True
        else:
            return False


def test_dpll():
    cnf = CNF(from_clauses=[(1, 2, 3), (-1, -2, -3)])
    assert test_result(cnf) == True


def test_dpll2():
    cnf = CNF(from_clauses=[(1, 2, 3), (-1, -2, -3), (-1, 2, 3)])
    assert test_result(cnf) == False
