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
        elif len(tokens) != 0 and tokens[0] == "p":
            # read the problem line
            for tok in tokens:
                num_vars = int(tokens[2])
                num_clauses = int(tokens[3])

    assert len(cnf[-1]) == 0
    cnf.pop()

    return cnf, num_vars, num_clauses


def get_pure_literals(cnf):
    literals = dict()
    pure_literals = dict()
    for clause in cnf:
        for lit in clause:
            if lit not in literals:
                literals[lit] = 1
            else:
                literals[lit] += 1
    for lit in literals:
        if literals[lit] == 1:
            pure_literals.add(lit)
    return pure_literals


def remove_pure_literal_clause(pure_literal, cnf):
    for lit in pure_literal:
        for clause in cnf:
            if lit in clause:
                cnf.remove(clause)
    return cnf


def dpll(cnf):
    # print(cnf)
    # get_pure_lit = get_pure_literals(cnf)
    # print(get_pure_lit)
    # get_pure_lit_clause = remove_pure_literal_clause(get_pure_lit, cnf)
    # print(get_pure_lit_clause)

    # while s contains a pure literal l:
    #    get_pure_lit = get_pure_literals(cnf)
    #    get_pure_lit_clause = remove_pure_literal_clause(get_pure_lit, cnf)

    while (get_pure_literals(cnf)):
        get_pure_lit = get_pure_literals(cnf)
        get_pure_lit_clause = remove_pure_literal_clause(get_pure_lit, cnf)
        cnf = get_pure_lit_clause
        print(cnf)


def main():
    file = "3sat_benchmark_problems/cnf_gen_3_12.cnf"
    with open(file, "r") as f:
        cnf = dimacs_parser(f)
    dpll(cnf)


if __name__ == "__main__":
    main()
