import argparse
from dimacs_parser import dimacs_parser

parser = argparse.ArgumentParser(
    description="Solve a CNF file using a SAT solver")
parser.add_argument("-m", "--method", help="SAT method to use",
                    choices=["dpll", "cdcl"], required=True)
parser.add_argument("-f", "--file", help="CNF file to solve",
                    required=False, default="random")
args = parser.parse_args()

if args.file != "random":
    file = args.file
    with open(file, "r") as f:
        cnf = dpll.dimacs_parser(f)
else:
    import CNF.cnf_generator as cnf_generator
    print("Please enter [num_variables] [num_clauses]: ", end="")
    num_var, num_clauses = map(int, input().split())

    filename = cnf_generator.generate_cnf(
        num_var, num_clauses)

    with open(filename, "r") as f:
        cnf = dimacs_parser(f)
        print(cnf)

if args.method == "dpll":
    from Solvers.dpll import dpll
    solver = dpll(cnf, cnf[0][0])
    # solver.dpll(cnf, cnf[0][0])
elif args.method == "cdcl":
    from Solvers.cdcl import cdcl
