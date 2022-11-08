# 1. Pick a variable without an assigned truth value. If there are none, return SAT

# 2. Assign the variable to a truth value (true or false)

# 3. Remove all clauses with positive literals of the variable assignment

# 4. Remove all negative literals of the variable assignment.

# 5. Keep performing unit propagation and pure literal elimination while possible

# 6. Check if an empty clause was created
#   if it was, try the other truth value backtrack
#   if it wasn't, go to step 1

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


def choose_variable(var):
    # choose a branching literal l occuring in cnf
    # todo: create heuristic for efficntly choosing variable
    # var = next(iter(var))
    lit = next(all_unassigned_vars([var]))
    return lit, True


def get_neg_lit(lit):
    return -(abs(lit))


def get_pos_lit(lit):
    return abs(lit)


def all_true(cnf):
    for clause in cnf:
        if len([lit for lit in clause if assign([lit])[lit] == "Assigned"]) == 0:
            return False
    return True


def some_false(cnf):
    for clause in cnf:
        if len([lit for lit in clause if assign([lit])[lit] == "Unassigned"]) == 0:
            return True
    return False


def assign(vars):
    return dict.fromkeys(list(vars), "Unassigned")


def are_all_variables_assigned(vars):
    # 1. Pick a variable without an assigned truth value. If there are none, return SAT
    all_assigned = all(var in assign(vars)
                       for var in vars)
    none_assigned = not any(var for var in vars if assign(vars)[
                            var] == "Unassigned")
    return all_assigned and none_assigned


def all_unassigned_vars(cnf):
    return filter(
        lambda v: v in assign([clause for clause in cnf]) and assign([clause for clause in cnf])[v] == "Unassigned", [clause for clause in cnf])


def remove_clauses_from_cnf_that_contain_positive_var(cnf, var, positive_clauses=[]):
    # 3. Remove all clauses with postive literals of the variable assignment.
    for clause in cnf:
        if var[0] not in clause:
            positive_clauses.append(clause)
    return positive_clauses


def remove_negative_literals_of_var(positive_clauses, var):
    # 4. Remove all negative literals of the variable assignment.
    new = []
    for clause in positive_clauses:
        if get_neg_lit(var[0]) in clause:
            new.append(
                tuple(filter(lambda item: item != get_neg_lit(var[0]), clause)))
        else:
            new.append(clause)

    positive_clauses = new
    return positive_clauses


def is_unit_clause(cnf):
    """
    Checks if clause is a unit clause. If and only if there is
    exactly 1 literal unassigned, and all the other literals having
    value of 0.
        :param clause: set of ints
        :returns: (is_clause_a_unit, the_literal_to_assign, the clause)
    """
    for clause in cnf:
        unassigned_literals = [lit for lit in clause if assign([lit])[
            lit] == "Unassigned"]
        if len(unassigned_literals) == 1:
            return True, unassigned_literals[0], clause
    return False, None, None


def unit_propagation(cnf):
    """
        A unit clause has all of its literals but 1 assigned to 0. Then, the sole
        unassigned literal must be assigned to value 1. Unit propagation is the
        process of iteratively applying the unit clause rule.
        :return: None if no conflict is detected, else return the literal
    """
    # 5. Keep performing unit propagation and pure literal elimination while possible
    while True:
        # 5.1. Unit propagation
        is_unit, lit, clause = is_unit_clause(cnf)
        if is_unit:
            # 5.1.1. Assign the literal to 1
            assign([lit])[lit] = "Assigned"
            # 5.1.2. Remove all clauses containing the literal
            cnf = remove_clauses_from_cnf_that_contain_positive_var(
                cnf, lit, [])
            # 5.1.3. Remove all clauses containing the negation of the literal
            cnf = remove_negative_literals_of_var(
                cnf, lit)
        else:
            break
    return cnf


def dpllr(cnf, vars, assignment):
    print(vars)
    if all_true(cnf):
        return True
    if some_false(cnf):
        return False
    # 1.
    while not are_all_variables_assigned(vars):
        # 2.
        var = choose_variable(vars)
        assign(vars)[var] = assignment
        # 3.
        print(var)
        cnf1 = remove_clauses_from_cnf_that_contain_positive_var(
            cnf, var, [])
        # 4.
        cnf2 = remove_negative_literals_of_var(
            cnf1, var)
        # # 5.
        cnf3 = unit_propagation(cnf2)
        for i in all_unassigned_vars(vars):
            print(i)
        break

        result = dpllr(cnf3, vars, assignment)
        if result == True:
            return result
        else:
            assign(vars)[var] = not assignment
            result = dpllr(cnf3, vars, assignment)
            if result == True:
                return result
            else:
                return False

        # 6.
        # if any(len(clause) == 0 for clause in cnf2):
        #     dpllr(cnf, vars, "Unassigned")
        # else:
        #     dpllr(cnf2, vars, "Assigned")

    return True


def dpll(cnf):
    print(cnf)
    vars = []
    for clause in cnf:
        for lit in clause:
            vars.append(lit)
    vars = list(set(vars))
    # sat_map = getsatmap(cnf)
    return dpllr(cnf, vars, "Assigned")
