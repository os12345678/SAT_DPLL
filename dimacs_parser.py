@staticmethod
def dimacs_parser(in_data):
    cnf = list()
    cnf.append(list())

    for line in in_data:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            # read the non-comment and non-problem lines
            for tok in tokens:
                lit = int(tok)
                if lit == 0:
                    cnf.append(list())
                else:
                    cnf[-1].append(lit)

    assert len(cnf[-1]) == 0
    cnf.pop()

    return cnf
