# DPLL: https://en.wikipedia.org/wiki/DPLL_algorithm

# function DPLL(cnf) returns true/false
# input: a set of clauses (cnf)
# output: a truth value indicating whether cnf is satisfiable

# def dpll(cnf):
#   while there is a unit clause {l} in cnf:
#       unit propagate
#   while there is a literal l that occurs pure in cnf:
#       pure literal eliminate
#   if cnf is empty:
#       return true
#   if cnf contains an empty clause:
#       return false
#   choose a branching literal l
#   return DPLL(cnf and {l}) or DPLL(cnf and {-l})

def pure_lit_elim(cnf, map):
    for var in [x for x in map if len(map[x]) == 0]:
        clause = frozenset((-var,))
        cnf.add(clause)
        map[-var].add(clause)


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


def getsatmap(cnf):
    map = dict()
    for clause in cnf:
        for x in clause:
            if x not in map:
                map[x] = set()
            map[x].add(clause)
    return map


def dpllr(cnf, map, solvedvars):
    if len(cnf) == 0:
        return True, solvedvars
    elif any(len(clause) == 0 for clause in cnf):
        return False, None
    while True:
        pure_lit_elim(cnf, map)
        s = unit_prop(cnf, map)
        solvedvars.extend(s)
        # if len(s) == 0:
        #     break
        x = next(iter(map))
        return dpllr(cnf and {x}, map, solvedvars + [x]) or dpllr(cnf and {-x}, map, solvedvars + [-x])


def dpll(cnf):
    map = getsatmap(cnf)
    return dpllr(cnf, map, [])


a = (1, 2, 3)
print(len(a))
