# input :: CNF file that gets converted to DIMACS file format.
# DIMACS is a line oriented format, consisting of 3 different basic types of lines.

#   A comment line. Any line that starts with "c" is comment line.

#   A summary line. This line contains information about the kind and size of the
#   problem within the file. A summary line starts with "p", continues with the
#   kind of the problem (in most cases "cnf"), the number of variables and the
#   number of clauses within this problem. Some DIMACS parsers expect this line
#   to be the first non-comment line, but some parsers can handle the file without
#   it.

#   A clause line. A clause line consists of space-separated numbers, ending with
#   a 0. Each non-zero number denotes a literal, with negative numbers being
#   negative literals of that variable, and 0 being the terminator of a line.

import itertools
import random
import readline
import time


def dimacs_parser(in_data):
    cnf = list()
    cnf.append(list())
    maxvar = 0

    for line in in_data:
        tokens = line.split()
        if len(tokens) != 0 and tokens[0] not in ("p", "c"):
            for tok in tokens:
                lit = int(tok)
                maxvar = max(maxvar, abs(lit))
                if lit == 0:
                    cnf.append(list())
                else:
                    cnf[-1].append(lit)
        # read the problem line
        elif len(tokens) != 0 and tokens[0] == "p":
            for tok in tokens:
                num_vars = int(tokens[2])
                num_clauses = int(tokens[3])

    assert len(cnf[-1]) == 0
    cnf.pop()

    return cnf, num_vars, num_clauses


# Approach 1: Brute Force / BDD
def brute_force(cnf):
    # Brute Force
    # 1. Generate all possible assignments
    # 2. Check if each assignment satisfies the CNF
    # 3. Return the first assignment that satisfies the CNF

    # Generate all possible assignments
    num_vars = 0
    for clause in cnf:
        for lit in clause:
            num_vars = max(num_vars, abs(lit))

    assignments = list()
    for i in range(2**num_vars):
        assignments.append(list())
        for j in range(num_vars):
            # right shift i by j bits and check if the last bit is 1
            assignments[i].append((i >> j) & 1)

    # Check if each assignment satisfies the CNF
    for assignment in assignments:
        # Check if each clause is satisfied
        for clause in cnf:
            # Check if the clause is satisfied
            clause_satisfied = False
            for lit in clause:
                if lit > 0 and assignment[lit - 1] == 1:
                    clause_satisfied = True
                    break
                if lit < 0 and assignment[-lit - 1] == 0:
                    clause_satisfied = True
                    break
            # If the clause is not satisfied, move on to the next assignment
            if not clause_satisfied:
                break
        # If all clauses are satisfied, return the assignment
        else:
            return assignment


# Approach 2: DPLL algorithm
def dpll(cnf):
    # DPLL algorithm
    # 1. If the CNF is empty, return True
    # 2. If the CNF contains an empty clause, return False
    # 3. If the CNF contains a unit clause, remove it and all its occurrences
    # 4. If the CNF contains a pure literal, remove it and all its occurrences
    # 5. Choose a variable and try to satisfy the CNF with it set to True
    # 6. If the CNF is satisfiable, return True
    # 7. Otherwise, try to satisfy the CNF with the variable set to False
    # 8. If the CNF is satisfiable, return True
    # 9. Otherwise, return False

    # If the CNF is empty, return True
    if len(cnf) == 0:
        return True

    # If the CNF contains an empty clause, return False
    for clause in cnf:
        if len(clause) == 0:
            return False

    # If the CNF contains a unit clause, remove it and all its occurrences
    for clause in cnf:
        if len(clause) == 1:
            lit = clause[0]
            cnf = remove_literal(cnf, lit)
            return dpll(cnf)

    # If the CNF contains a pure literal, remove it and all its occurrences
    for lit in get_pure_literals(cnf):
        cnf = remove_literal(cnf, lit)
        return dpll(cnf)

    # Choose a variable and try to satisfy the CNF with it set to True
    lit = get_random_literal(cnf)
    cnf1 = remove_literal(cnf, lit)
    result = dpll(cnf1)
    # If the CNF is satisfiable, return True
    if result:
        return True
    # Otherwise, try to satisfy the CNF with the variable set to False
    else:
        cnf2 = remove_literal(cnf, -lit)
        return dpll(cnf2)


def get_pure_literals(cnf):
    pure_literals = set()
    for clause in cnf:
        for lit in clause:
            if -lit not in pure_literals:
                pure_literals.add(lit)
            else:
                pure_literals.remove(-lit)
    return pure_literals


def get_random_literal(cnf):
    literals = set()
    for clause in cnf:
        for lit in clause:
            literals.add(lit)
    return random.choice(list(literals))


def remove_literal(cnf, lit):
    new_cnf = list()
    for clause in cnf:
        if lit not in clause:
            new_clause = list()
            for l in clause:
                if l != -lit:
                    new_clause.append(l)
            new_cnf.append(new_clause)
    return new_cnf


def main():
    file = "3sat_benchmark_problems/sat_2000.cnf"
    with open(file, "r") as f:
        cnf, num_var, num_clauses = dimacs_parser(f)

    print(f"CNF: {file}")
    print(f"Problem: {len(cnf[0])}-Sat")
    print(f"Number of variables: {num_var}")
    print(f"Number of clauses: {num_clauses} \n")

    # print("Brute Force:")
    # start_time = time.time()
    # assignment = brute_force(cnf)
    # end_time = time.time()
    # if assignment is not None:
    #     print("Result: SATisfiable")
    #     print("Assignment:", assignment)
    # else:
    #     print("Result: UNSATisfiable")
    # print("Time taken:", end_time - start_time)
    # print()

    print("DPLL:")
    start_time = time.time()
    result = dpll(cnf)
    end_time = time.time()
    if result:
        print("Result: SATisfiable")
        print("Assignment:",)
    else:
        print("Result: UNSATisfiable")
    print("Time taken:", end_time - start_time)
    print()


if __name__ == "__main__":
    main()
