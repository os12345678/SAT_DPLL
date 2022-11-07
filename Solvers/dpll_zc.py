def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]


# CNF = full list of clauses (tuples)
# assignments = variable assignments
def dpll(cnf, assignments={}):

    # [
    #   {("p", True), ("q", False)},
    #   {("p", True), ("r", True)}.
    #   {("p", False), ("r", True)}
    # ]

    # if theres no clauses, therefore true
    if len(cnf) == 0:
        return True, assignments

    # if a clause is empty, it can't be satisfied
    if any([len(c) == 0 for c in cnf]):
        return False, None

    # Gets first literal in the first clause -> "p"
    l = __select_literal(cnf)

   # c = {("p", True), ("q", False)}

    new_cnf = [c for c in cnf if (l, True) not in c]

    # for clause in cnf:
    #     if ("p", True) not in clause:
    #         return c

    # [{("p", False), ("r", True)}]

    new_cnf = [c.difference({(l, False)}) for c in new_cnf]

    # # for c in new_cnf:
    # #     return c.difference({("p", False)})

    # # [{("r", True)}]

    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    # if both options don't work - its unsat
    return False, None


# go through each literal
# set the literal to true first
#   extract out the clauses where p = false
#   run the algorithm again until one of the first 2 comparisons returns (no clauses or 1 clause is empty)
#   if an answer is found return
# otherwise, set literal to false
#   repeat same steps

# if both options dont work, then we return False, none at the end as its unsatisfiable

def recursive_dpll(clauses):
    """ function to run a backtracking dpll based algorithm

        clauses: list of cnf clauses in tuple form
        assigned: dictionary with variable assignments
    """
    # 0. if any empty clauses exist, unsat
    for clause in clauses:
        if len(clause) == 0:
            return False

    # 1. Pick a variable without an assigned truth value. If there are none, return SAT
    if len(clauses) == 0:
        # no more clauses, therefore all have been reduced
        return True  # return SAT

    print("clauses: ", clauses)
    # get the first literal we see - can be optimised to find most frequent literal
    literal = abs(clauses[0][0])
    print("literal: ", literal)
    # 2. Assign it a truth-value

    # if we start with true, we'll need to iteratively remove all clauses with occurence of the literal

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

    positive_clauses = new

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
    if sat:
        print("positive worked, we did it boys")
        return sat

    # 3. Remove all clauses with postive literals of the variable assignment
    negative_clauses = []
    for clause in clauses:
        if -(literal) not in clause:
            negative_clauses.append(clause)

    # 4. Remove all negative literals of the variable assignment.
    new = []
    for clause in negative_clauses:
        if literal in clause:
            new.append(
                tuple(filter(lambda item: item == -(literal), clause)))
        else:
            new.append(clause)

    # otherwise we need to do the literal as false
    sat = recursive_dpll(negative_clauses)
    if sat:
        print("negative worked, we did it boys")
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
