import argparse

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
        cnf, num_var, num_clauses = dimacs_parser(f)
else:
    import cnf_generator
    print("Please enter [num_variables] [num_clauses]: ", end="")
    num_var, num_clauses = map(int, input().split())

    filename = cnf_generator.generate_cnf(
        num_var, num_clauses)

if args.method == "dpll":
    from dpll import dpll
    from dpll import dimacs_parser
elif args.method == "cdcl":
    from cdcl import cdcl
    from cdcl import dimacs_parser
