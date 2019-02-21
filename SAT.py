import argparse
from sat_solve import solve
from cnf import CNF


def write_sol_to_file(cnf, output_file):
	"""
	Write solution of a SAT problem to a file
	:param output_file: Output file name
	:return: None
	"""
	with open(output_file, 'w') as f:
		for variable in cnf.variables:
			f.write(str(cnf.assign[variable] * variable) + " 0\n")
	f.close()		


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-S1', action='store_true', help='Vanilla Davis Putnam')
	parser.add_argument('-S2', action='store_true', help='UP heuristic')
	parser.add_argument('-S3', action='store_true', help='LEFV heuristic')
	parser.add_argument('inputfile', help="Input file containing SAT problem in DIMACS form")
	args = vars(parser.parse_args())
	if args['S1'] == args['S2'] == args['S3'] == False:
		parser.print_help()
		parser.exit(1)

	input_file = args['inputfile']
	output_file = 'solution.txt'

	with open(input_file) as f:
		dimacs_str = f.read()

	if args['S1'] == True:
		heuristic = None
	elif args['S2'] == True:
		heuristic = 'UP'
	elif args['S3'] == True:
		heuristic = 'lefv' 		

	cnf = CNF(dimacs_str)

	# TO-DO
	# The solve() method uses global variables 'splits' and 'backtracks'. It is undefined when called from here. Need to fix

	if solve(cnf, heuristic):
		print("Problem is satisfiable. Solution written to %s" % output_file)
		write_sol_to_file(cnf, output_file)
	else:
		print("Problem is unsatisfiable")
						