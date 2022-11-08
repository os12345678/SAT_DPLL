import argparse
import time
from dimacs_parser import dimacs_parser

parser = argparse.ArgumentParser(
    description="Solve a CNF file using a SAT solver")
parser.add_argument("-m", "--method", help="SAT method to use",
                    choices=["dpll", "dpll100", "cdcl", "brute", "test"], required=True)
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

if args.method == "test":
    from Solvers.dpll import dpll
    res = dpll(cnf)
    print(res)

if args.method == "dpll":
    from Solvers.dpll_zc import recursive_dpll
    from tests.test import test_result
    dpll_solver = recursive_dpll(cnf)
    print("our result:", dpll_solver)
    test_solver = test_result(cnf)
    print("actual: ", test_solver)

if args.method == "dpll100":
    from Solvers.dpll import dpll
    from tests.test import test_result
    import glob

    failed = []
    unsat = glob.glob("CNF/examples/UUF50.218.1000/*.cnf")
    sat = glob.glob("CNF/examples/uf50-218/*.cnf")
    i = 0
    for file in sat:
        if i == 100:
            break
        with open(file, "r") as f:
            random_cnf_ = dimacs_parser(f)
        dpll_solver = dpll(random_cnf_)
        i += 1
        pysat_result = test_result(random_cnf_)
        if dpll_solver != pysat_result:
            failed.append(cnf)
    print(f'sat cases: {len(failed)} failed')
    j = 0
    for file in unsat:
        if j == 100:
            break
        with open(file, "r") as f:
            random_cnf_ = dimacs_parser(f)
        dpll_solver = dpll(random_cnf_)
        j += 1
        pysat_result = test_result(random_cnf_)
        if dpll_solver != pysat_result:
            failed.append(cnf)
    print(f'unsatsat cases: {len(failed)} failed')
    # print(failed)

elif args.method == "cdcl":
    from Solvers.cdcl import cdcl
elif args.method == "brute":
    from Solvers.brute_force import brute_force
    start = time.time()
    brute_solver = brute_force(cnf)
    print(time.time() - start)
    print(brute_solver)
