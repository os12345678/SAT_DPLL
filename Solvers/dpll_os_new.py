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
    # todo: create heuristic for choosing variable
    var = next(all_unassigned_vars(var))
    return var, True


def get_neg_lit(lit):
    return -(abs(lit))


def get_pos_lit(lit):
    return abs(lit)


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


def unit_propagation(cnf, map):
    """
        A unit clause has all of its literals but 1 assigned to 0. Then, the sole
        unassigned literal must be assigned to value 1. Unit propagation is the
        process of iteratively applying the unit clause rule.
        :return: None if no conflict is detected, else return the literal
    """
    # 5. Keep performing unit propagation and pure literal elimination while possible
    pass


def dpllr(cnf, map):
    print(cnf)
    vars = []
    for clause in cnf:
        for lit in clause:
            vars.append(lit)
    vars = list(set(vars))

    # 1.
    while not are_all_variables_assigned(vars):
        # 2.
        var = choose_variable(vars)
        assign(vars)[var] = "Assigned"
        # 3.
        print(var)
        clauses_from_cnf_that_dont_contain_positive_var = remove_clauses_from_cnf_that_contain_positive_var(
            cnf, var, [])
        # 4.
        clauses_from_cnf_that_dont_contain_neg_var = remove_negative_literals_of_var(
            clauses_from_cnf_that_dont_contain_positive_var, var)
        print(clauses_from_cnf_that_dont_contain_neg_var)

        break

    return "SAT"


def dpll(cnf):
    sat_map = getsatmap(cnf)
    return dpllr(cnf, sat_map)
