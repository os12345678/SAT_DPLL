@staticmethod
def dimacs_parser(in_data):
    cnf = list()
    # cnf.append(tuple())

    for line in in_data:
        tokens = line.split()
        if tokens[0] == "%":
            break
        if len(tokens) == 0 or tokens[0] in ("p", "c"):
            continue
        cnf.append(tuple(int(tok) for tok in tokens if tok != "0"))

    return cnf
