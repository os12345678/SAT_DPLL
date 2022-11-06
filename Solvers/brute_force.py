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
            # num_vars! assignments
            assignments[i].append((i >> j) & 1)

    # Check if each assignment satisfies the CNF
    for assignment in assignments:
        # Check if each clause is satisfied
        for clause in cnf:
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
                return "UNSAT"
        # If all clauses are satisfied, return the assignment
        else:
            # return assignment
            return "SAT"
