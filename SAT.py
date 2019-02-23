import argparse
from sat_solve import SATSolver
from cnf import CNF


def write_sol_to_file(cnf, output_file, satisfiable=True):
    """
    Write solution of a SAT problem to a file
    :param cnf: CNF object
    :param output_file: Output file name
    :param satisfiable: Boolean indicating whether the problem was satisfiable or not
    :return: None
    """
    with open(output_file, 'w') as f:
        if satisfiable:
            for variable in cnf.variables:
                f.write(str(cnf.assign[variable] * variable) + " 0\n")
        else:
            f.write("")
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-S1', action='store_true', help='Vanilla Davis Putnam')
    parser.add_argument('-S2', action='store_true', help='UP heuristic')
    parser.add_argument('-S3', action='store_true', help='LEFV heuristic')
    parser.add_argument('inputfile', help="Input file containing SAT problem in DIMACS form")
    args = vars(parser.parse_args())
    if args['S1'] == args['S2'] == args['S3'] is False:
        parser.print_help()
        parser.exit(1)

    input_file = args['inputfile']
    output_file = input_file.split('.')[0] + '.out'

    with open(input_file) as f:
        dimacs_str = f.read()

    if args['S1'] is True:
        heuristic = None
    elif args['S2'] is True:
        heuristic = 'UP'
    elif args['S3'] is True:
        heuristic = 'lefv'

    cnf = CNF(dimacs_str)
    sat_solver = SATSolver(heuristic=heuristic)

    if sat_solver.solve(cnf):
        write_sol_to_file(cnf, output_file, satisfiable=True)
        print("Problem is satisfiable. Solution written to %s" % output_file)
    else:
        write_sol_to_file(cnf, output_file, satisfiable=False)
        print("Problem is unsatisfiable")
