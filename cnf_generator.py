# Generate valid cnf files with the following command:
# python cnf_generator.py [variables] [clauses] > cnf_gen_[variables]_[clauses].txt

import argparse
import random
import os

parser = argparse.ArgumentParser(
    description='Generate a valid cnf file used for 3sat.py')

parser.add_argument('--variables', '-v', dest='number_of_variables', default=3, type=int, required=False,
                    help="Number of variable.")
parser.add_argument('--clauses', '-c', dest='number_of_clauses', default=5, type=int, required=False,
                    help="Number of clauses.")

args = parser.parse_args()

filename = f"3sat_benchmark_problems/cnf_gen_{args.number_of_variables}_{args.number_of_clauses}.cnf"

with open(filename, 'w') as f:
    f.write(f"c User generated cnf file\n")
    f.write(f"p cnf {args.number_of_variables} {args.number_of_clauses}\n")
    for i in range(args.number_of_clauses):
        # Generate a random clause
        clause = [random.randint(1, args.number_of_variables)
                  for i in range(3)]
        # Randomly negate a literal
        clause[random.randint(0, 2)] *= -1
        f.write(f"{clause[0]} {clause[1]} {clause[2]} 0 \n")
