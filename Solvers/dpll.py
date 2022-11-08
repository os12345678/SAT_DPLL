import random


def getsatmap(cnf):
    map = {}
    for clause in cnf:
        for lit in clause:
            if lit not in map:
                map[lit] = set()
            if -lit not in map:
                map[-lit] = set()
            map[lit].add(clause)
    return map


def is_int(clause):
    return type(clause) == int


def contains_unit_clause(cnf):
    # check if a unit clause exists (tuple with len(1) is an int)
    for clause in cnf:
        if type(clause) == int:
            return clause
    return False


def unit_propagate(cnf, lit):
    # if unit clause exists, remove all clauses that contain it
    new = []
    for clause in cnf:
        if lit not in clause:
            new.append(tuple(clause))
    return new


def contains_pure(map):
    # check if there exists a literal l where only l or only -l occurs in cnf
    for key in map.keys():
        if -key not in map:
            return key
    return False


def get_pure_lit(cnf, lit):
    # if a pure lit exists, remove it and all its occurrences
    new = []
    for clause in cnf:
        if lit in clause:
            new.append(
                tuple(filter(lambda item: item != lit, clause)))
        else:
            new.append(clause)
    return new


def dpllr(cnf, map):
    # while there is a unit clause {l} in Φ do
    #     cnf ← unit-propagate(l, cnf);
    unit = contains_unit_clause(cnf)
    print("unit", unit)
    while unit:
        cnf = unit_propagate(cnf, unit)

    # while there is a literal l that occurs pure in Φ do
    #     Φ ← pure-literal-assign(l, Φ);
    pure = contains_pure(map)
    print("pure", pure)
    while pure:
        cnf = get_pure_lit(cnf, pure)

    # if Φ is empty then return true;
    if len(cnf) == 0:
        return True

    # if Φ contains an empty clause then return false;
    for clause in cnf:
        if len(clause) == 0:
            return False

    # l ← choose-literal(Φ);
    # l = random.choice(list(map.keys()))  # todo: improve choose heuristic
    l = cnf[0][0]

    # return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {not(l)});
    sat = dpllr(cnf + [(l,)], map)
    if sat:
        return True
    return dpllr(cnf + [(-l,)], map)


def dpll(cnf):
    map = getsatmap(cnf)
    return dpllr(cnf, map)
