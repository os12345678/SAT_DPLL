def getsatmap(clauses):
    map = dict()
    for clause in clauses:
        for x in clause:
            if x not in map:
                map[x] = set()
            map[x].add(clause)
    return map


def unit_prop(clauses, map):
    solvedvars = []
    for clause in [c for c in clauses if len(c) == 1]:
        x = next(iter(clause))
        solvedvars.append(x)
        if not x in map:
            continue
        for c in map[x]:
            for y in c:
                if y == x:
                    continue
                map[y].remove(c)
            clauses.remove(c)
        for c in map[-x]:
            newc = c - {-x}
            clauses.remove(c)
            clauses.add(newc)
            for y in c:
                if y == -x:
                    continue
                map[y].remove(c)
                map[y].add(newc)
        del map[x]
        del map[-x]
    return solvedvars


def pure_lit_elim(clauses, map):
    solvedvars = []
    for var in [x for x in map if len(map[x]) == 0]:
        clauses.add(frozenset({-var}))
        solvedvars.append(var)
    return solvedvars


def tauntology(clauses, map):
    for m in [m for m in map if m > 0]:
        for c in [c for c in map[m] if c in map[-m]]:
            clauses.remove(c)
            for y in c:
                map[y].remove(c)
        if len(map[m]) == 0 and len(map[-m]) == 0:
            del map[m]
            del map[-m]


def dpll(clauses):
    clauses = {frozenset(c) for c in clauses}
    map = getsatmap(clauses)
    print(map)
    solvedvars = []
    while True:
        solvedvars.extend(unit_prop(clauses, map))
        solvedvars.extend(pure_lit_elim(clauses, map))
        tauntology(clauses, map)
        if len(clauses) == 0:
            return "SAT"
        if len(clauses) == 1 and len(next(iter(clauses))) == 0:
            return "UNSAT"
        if len(clauses) == 0 or len(map) == 0:
            break
        x = next(iter(map))
        clauses.add(frozenset({x}))
        clauses.add(frozenset({-x}))
        map[x] = set()
        map[-x] = set()
    return "SAT"
