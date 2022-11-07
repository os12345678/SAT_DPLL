# Generate valid cnf files with the following command:
# python cnf_generator.py [variables] [clauses] > cnf_gen_[variables]_[clauses].txt

import random


def generate_cnf(num_var, num_clauses):
    filename = f"CNF/Examples/cnf_gen_{num_var}_{num_clauses}.cnf"

    with open(filename, 'w') as f:
        f.write(f"c User generated cnf file\n")
        f.write(f"p cnf {num_var} {num_clauses}\n")
        for i in range(num_clauses):
            # Generate a random clause
            clause = [random.randint(1, num_var)
                      for i in range(3)]
            # Randomly negate a literal
            clause[random.randint(0, 2)] *= -1
            f.write(f"{clause[0]} {clause[1]} {clause[2]} 0 \n")

    return filename


def random_kcnf(n_literals, n_conjuncts, k=3):
    result = []
    for _ in range(n_conjuncts):
        conj = tuple()
        for _ in range(k):
            index = random.randint(0, n_literals)
            conj.add((
                str(index).rjust(10, '0'),
                bool(random.randint(0, 2)),
            ))
        result.append(conj)
    return result


if __name__ == "__main__":
    random_kcnf()
