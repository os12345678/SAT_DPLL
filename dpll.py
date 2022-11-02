from copy import deepcopy


def dimacs_parser(in_data):
    cnf = list()
    cnf.append(list())
    maxvar = 0

    for line in in_data:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            # read the non-comment and non-problem lines
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


def dpll(cnf):
    remove_unit_clause(cnf)
    remove_pure_literal_clause(
        get_pure_literals(cnf), cnf)
    if len(cnf) == 0:
        return True
    for clause in cnf:
        if len(clause) == 0:
            return False
    return dpll(cnf)


def main():
    file = "3sat_benchmark_problems/sat_20.cnf"
    with open(file, "r") as f:
        cnf = dimacs_parser(f)
    dpll(cnf)


if __name__ == "__main__":
    main()
