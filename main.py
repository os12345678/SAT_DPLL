import argparse
import time
from dimacs_parser import dimacs_parser
import random
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt


parser = argparse.ArgumentParser(
    description="Solve a CNF file using a SAT solver")
parser.add_argument("-m", "--method", help="SAT method to use",
                    choices=["dpll", "dpll100", "brute", "compare"], required=True)
parser.add_argument("-f", "--file", help="CNF file to solve",
                    required=False, default="random")
args = parser.parse_args()

if args.file != "random":
    file = args.file
    with open(file, "r") as f:
        cnf = dimacs_parser(f)
else:
    import CNF.cnf_generator as cnf_generator
    print("Please enter [num_variables] [num_clauses]: ", end="")
    num_var, num_clauses = map(int, input().split())

    filename = cnf_generator.generate_cnf(
        num_var, num_clauses)

    with open(filename, "r") as f:
        cnf = dimacs_parser(f)

if args.method == "dpll":
    from Solvers.dpll import dpll
    from tests.test import test_result
    dpll_solver = dpll(cnf)
    print("our result:", dpll_solver)
    test_solver = test_result(cnf)
    print("actual result: ", test_solver)

if args.method == "compare":
    from Solvers.brute_force import brute_force
    from Solvers.dpll import dpll
    import CNF.cnf_generator as cnf_generator

    brute_force_times = []
    dpll_times = []
    for n_literals in range(16):
        current_brute_force_times = []
        current_dpll_times = []
        for _ in range(100):
            n_conjuncts = random.randint(0, n_literals*6)
            filename = cnf_generator.generate_cnf(
                n_literals, n_conjuncts)
            with open(filename, "r") as f:
                s = dimacs_parser(f)

            start = time.time()
            brute_force(s)
            stop = time.time()
            current_brute_force_times.append(stop-start)
            start = time.time()
            dpll(s)
            stop = time.time()
            current_dpll_times.append(stop-start)

        brute_force_times.append(np.mean(current_brute_force_times))
        dpll_times.append(np.mean(current_dpll_times))

    df = pd.DataFrame(
        {'Number of literals': range(16),
         'Brute Force': brute_force_times,
         'DPLL': dpll_times
         }
    )
    sns.set()
    viz = df.plot(x='Number of literals')
    viz.set_ylabel("Time (Seconds)")
    plt.show()


if args.method == "dpll100":
    from Solvers.dpll import dpll
    from tests.test import test_result
    import glob

    failed = []
    unsat = glob.glob("CNF/examples/UUF50.218.1000/*.cnf")
    sat = glob.glob("CNF/examples/uf50-218/*.cnf")
    i = 0
    for file in sat:
        if i == 5:
            break
        with open(file, "r") as f:
            random_cnf_ = dimacs_parser(f)
        dpll_solver = dpll(random_cnf_)
        print("our result:", dpll_solver)
        i += 1
        pysat_result = test_result(random_cnf_)
        print("actual result: ", pysat_result)
        if dpll_solver != pysat_result:
            failed.append(cnf)
    print(f'sat cases: {len(failed)} failed')
    j = 0
    for file in unsat:
        if j == 5:
            break
        with open(file, "r") as f:
            random_cnf_ = dimacs_parser(f)
        dpll_solver = dpll(random_cnf_)
        print("our resutl:", dpll_solver)
        j += 1
        pysat_result = test_result(random_cnf_)
        print("actual result:", pysat_result)
        if str(dpll_solver) != str(pysat_result):
            failed.append(cnf)
    print(f'unsat cases: {len(failed)} failed')
    # print(failed)

# elif args.method == "cdcl":
#     from Solvers.cdcl import cdcl
#     cdcl_solver = cdcl(cnf)
elif args.method == "brute":
    from Solvers.brute_force import brute_force
    start = time.time()
    brute_solver = brute_force(cnf)
    print(time.time() - start)
    print(brute_solver)
