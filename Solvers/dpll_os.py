# DPLL algorithm

# boolean DPPL(cnf):
# while cnf contains a unit clause {l}:
#     delete from cnf all clauses containing l
#     delete -l from all clauses in cnf

# if there is a clause with length 0:
#   return False

# while cnf contains a pure literal l:
#   delete from cnf all clauses containing l

# if cnf is empty:
#   return True

# choose a branching literal l occuring in cnf

# if DPPL(cnf or {l}) is True:
#   return True

# if DPPL(cnf or {-l}) is True:
#   return True

# return False

def create_map(cnf):
    map = dict()
    for clause in cnf:
        for lit in clause:
            if lit not in map:
                map[lit] = set()
            if -lit not in map:
                map[-lit] = set()
            map[lit].add(clause)
    return map


# unit propagation notes:
# Given a partial truth assignment φ and a set of clauses F identify all the
# unit clauses, extend the partial truth assignment, repeat until fix-point.


def contains_unit_clause(cnf):
    unit_clause = []
    for clause in cnf:
        if len(clause) == 1:
            unit_clause.append(clause)
    return unit_clause if unit_clause else False


def remove_unit_clause(cnf, unit_clause):
    # delete from cnf all clauses containing l
    # delete -l from all clauses in cnf
    for unit in unit_clause:
        for litu in unit:
            for clause in cnf:
                for litc in clause:
                    if litc == litu:
                        print(litc)
                        break
                    break
                break
            break
        break


def pure_literal_elim(cnf, map, pure_lit=[]):
    for key, value in map.items():
        if len(value) == 1:  # pure literal
            # delete from cnf all clauses containing key
            pure_lit.append(key)
    for clause in [c for c in cnf]:
        for lit in clause:
            if lit in pure_lit:
                cnf.remove(clause)
    return cnf


def dpll(cnf):
    map = create_map(cnf)
    for key, val in map.items():
        print(key, val)
    # while contains_unit_clause(cnf):
    #     unit_clause = contains_unit_clause(cnf)
    #     updated_cnf = remove_unit_clause(cnf, unit_clause)
    # print("cnf after unit clause elim: ", updated_cnf)
    return

    # if len(cnf) == 0:
    #     return "SAT"
    # elif any(len(c) == 0 for c in cnf):
    #     return "UNSAT"

    # while pure_literal_elim(cnf, map):
    #     pure_literal_elim(cnf, map)

    # branch_lit = next(iter(cnf))
    # return dpll(cnf | {branch_lit}) or dpll(cnf | {-branch_lit})

    # return
