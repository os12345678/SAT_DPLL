

def compliment(assignment):
    new = []
    for clause in assignment:
        new_clause = []
        for literal in clause:
            new_clause.append(-literal)
        new.append(tuple(new_clause))

    return new


def recursive_dpll(clauses):
    """ function to run a backtracking dpll based algorithm

        clauses: list of cnf clauses in tuple form
        assigned: dictionary with variable assignments
    """

    # 1. if reduced to empty set, sat
    if len(clauses) == 0:
        return True  # return SAT

    # 0. if any empty clauses exist, unsat
    for clause in clauses:
        if len(clause) == 0:
            return False

    literal = clauses[0][0]

    # 3. Remove all clauses with postive literals of the variable assignment
    positive_clauses = []
    for clause in clauses:
        if literal not in clause:
            positive_clauses.append(clause)

    # 4. Remove all negative literals of the variable assignment.

    new = []
    for clause in positive_clauses:
        if -(literal) in clause:
            new.append(
                tuple(filter(lambda item: item != -(literal), clause)))
        else:
            new.append(clause)

    # print("literal:", literal)

    # print("POSITIVE REDUCTION")
    # print("prior:", positive_clauses, len(positive_clauses))
    # print("after:", new, len(new))
    positive_clauses = new
    # print("positive:", positive_clauses)
    # print("new:", new)
    # print("clauses:", clauses)

    # 5. Keep performing unit propogation and pure literal elimination while possible

    # skipped for now
    """
    Unit clause: Checks if clause is a unit clause. If and only if there is
    exactly 1 literal unassigned, and all the other literals having
    value of 0.
        :param clause: set of ints
        :returns: (is_clause_a_unit, the_literal_to_assign, the clause)
    
    Unit prop: A unit clause has all of its literals but 1 assigned to 0. Then, the sole
    unassigned literal must be assigned to value 1. Unit propagation is the
    process of iteratively applying the unit clause rule.
    :return: None if no conflict is detected, else return the literal
    """

    # 6. Check if an empty clause was created

    sat = recursive_dpll(positive_clauses)
    # print("positive sat:", sat)
    if sat:
        # print("positive worked, we did it boys")
        return sat

    # # 3. Remove all clauses with postive literals of the variable assignment
    # negative_clauses = []
    # for clause in clauses:
    #     if -(literal) not in clause:
    #         negative_clauses.append(clause)

    # # 4. Remove all negative literals of the variable assignment.
    # new = []
    # for clause in negative_clauses:
    #     if literal in clause:
    #         new.append(
    #             tuple(filter(lambda item: item == literal, clause)))
    #     else:
    #         new.append(clause)

    # print("NEGATIVE REDUCTION")
    # print("prior:", nega, len(negative_clauses))
    # print("after:", new, len(new))
    # positive_clauses = new
    # print("negative:", negative_clauses)
    # print("new:", new)
    # print("clauses:", clauses)

    # otherwise we need to do the literal as false
    else:
        sat = recursive_dpll(compliment(positive_clauses))
        # print("negative sat:", sat)
        if sat:
            # print("negative worked, we did it boys")
            return sat

    return False


def test(clauses):
    from pysat.formula import CNF
    from pysat.solvers import Solver

    with Solver(bootstrap_with=clauses) as solver:
        # 1.1 call the solver for this formula:
        print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

        # 1.2 the formula is satisfiable and so has a model:
        print('and the model is:', solver.get_model())
