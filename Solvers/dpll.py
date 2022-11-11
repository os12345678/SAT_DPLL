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


def pick_branching_literal(map):
    maxcount = max(len(v) for v in map.values())
    return next(k for k, v in map.items() if len(v) == maxcount)


def reduce_cnf(cnf, lit):
    return get_pure_lit(unit_propagate(cnf, lit), -lit)


def dpllr(cnf, map, values):
    # while there is a unit clause {l} in Φ do
    #     cnf ← unit-propagate(l, cnf);
    unit = contains_unit_clause(cnf)

    while unit:
        cnf = unit_propagate(cnf, unit)

    # while there is a literal l that occurs pure in Φ do
    #     Φ ← pure-literal-assign(l, Φ);
    pure = contains_pure(map)
    while pure:
        cnf = get_pure_lit(cnf, pure)

    # if Φ is empty then return true;
    if len(cnf) == 0:
        return True, values

    # if Φ contains an empty clause then return false;
    for clause in cnf:
        if len(clause) == 0:
            return False, values

    # l ← choose-literal(Φ);
    l = pick_branching_literal(map)  # todo: improve branching heuristic

    # return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {not(l)});
    # replace every occurrence of l with "true" and every occurrence of not l with "false" in the formula Φ, and simplify the resulting formula
    # test with literal set to true
    sat, values = dpll(reduce_cnf(cnf, l), {**values, **{l: True}})
    if sat:
        return sat, values

    # otherwise test with literal set to false
    sat, values = dpll(reduce_cnf(cnf, l), {**values, **{l: False}})
    if sat:
        return sat, values

    return False, values


def dpll(cnf, values={}):
    map = getsatmap(cnf)
    return dpllr(cnf, map, values)
