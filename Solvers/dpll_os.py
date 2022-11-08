# DPLL: wikipedia.org/wiki/DPLL_algorithm

# 1. Check recursive base cases
#     1.1. if cnf is empty -> SAT
#     1.2. if cnf contains empty clauses -> UNSAT
# 2. Pure literal elimination
# 3. Unit propagation
# 4. Choose a branching literal l
# 5. Backtrack on l and -l


def compliment(assignment):
    # returns the compliment of each assignment literal (i.e -1 -> 1, 1 -> -1)
    for i, lit in enumerate(assignment):
        assignment[i] = -lit
    return assignment


def sat(cnf, assignment):
    # if all clauses have at least one true literal
    for clause in cnf:
        if len([lit for lit in clause if lit in assignment]) == 0:
            return False
    return True


def unsat(cnf, assignment):
    # if any clause has no true literals
    assignment_comp = compliment(assignment)
    for clause in cnf:
        if len([lit for lit in clause if lit not in assignment_comp]) == 0:
            return True
    return False


def pure_literal_elim(cnf, assignment):
    assignment_comp = compliment(assignment)
    candidates = []
    for clause in cnf:
        if len([var for var in clause if var in assignment]) == 0:
            candidates = candidates + [var for var in clause]
    candidates_comp = compliment(candidates)
    pure_literals = [var for var in candidates if var not in candidates_comp]
    for var in pure_literals:
        if var not in assignment and var not in assignment_comp:
            return var
    return False


def unit_prop(cnf, assignment):
    assignment_comp = compliment(assignment)
    for clause in cnf:
        remaining = [var for var in clause if var not in assignment_comp]
        if len(remaining) == 1:
            if remaining[0] not in assignment:
                return remaining[0]
    return False


def choose_branching_literal(cnf, assignment):
    # choose a branching literal l not in assignment or the compliment of assignment
    literal_not_in_assignment = assignment + compliment(assignment)
    for clause in cnf:
        for lit in clause:
            if lit not in literal_not_in_assignment:
                return lit
    return False


def dpllr(cnf, assignment):
    print(cnf)
    # base cases
    # if len(cnf) == 0:
    #     return True
    # elif any([len(clause) == 0 for clause in cnf]):
    #     return False
    if sat(cnf, assignment):
        return True
    elif unsat(cnf, assignment):
        return False

    # pure literal elimination
    pure_literal = pure_literal_elim(cnf, assignment)
    print("pure literal: ", pure_literal)
    if pure_literal:
        dpllr(cnf, assignment + [pure_literal])

    # unit propagation
    unit_literal = unit_prop(cnf, assignment)
    print("unit literal: ", unit_literal)
    if unit_literal:
        dpllr(cnf, assignment + [unit_literal])

    # choose branching literal
    branching_literal = choose_branching_literal(cnf, assignment)
    print("branching literal: ", branching_literal)
    if branching_literal:
        print("assignment + [branching_literal]: ",
              assignment + [branching_literal])
        # backtrack on l or -l
        result = dpllr(cnf, assignment + [branching_literal])
        if result:
            return result
        else:
            result = dpllr(cnf, assignment + [-branching_literal])
            if result:
                return result
            else:
                return False

    # backtracking


def dpll(cnf):
    return dpllr(cnf, [])
