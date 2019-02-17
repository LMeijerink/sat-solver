import time
from cnf import CNF
import numpy as np
import copy


def solve(cnf):
    """
    Solve a SAT problem
    :param cnf: Object containing the problem in closed normal form
    :return: True if solvable else False
    """
    cnf.simplify()
    if cnf.clauses == []:
        cnf.print_sol()
        return True
    if [] in cnf.clauses:
        return False
    # Split
    s = cnf.random_split()
    cnf1 = copy.deepcopy(cnf)
    cnf1.clauses += [[s]]
    if solve(cnf1):
        return True
    else:
        cnf2 = copy.deepcopy(cnf)
        cnf2.clauses += [[-s]]
        if solve(cnf2):
            return True
    return False


def sudokus_to_DIMACS(filename, rules):
    """
    Takes in file of sudokus and returns a list of puzzles in DIMACS format
    :param filename: Filename of sudoku problems
    :param rules: String of sudoku rules
    :return: String containing rules and sudoku problems in DIMACS format
    """
    puzzles = []
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            line = np.array(list(line))
            matrix = np.reshape(line, (9, 9))
            clauses = rules
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if matrix[x, y] != '.':
                        clauses += str(x + 1) + str(y + 1) + matrix[x, y] + ' 0\n'
            puzzles += [clauses]
    return puzzles


if __name__ == '__main__':
    start_time = time.time()
    sudokufile = '1000 sudokus.txt'
    n_puzzles = 10

    # Load in rules, same for every sudoku
    with open('sudoku-rules.txt') as f:
        rules = f.read()

    example_puzzles = sudokus_to_DIMACS(sudokufile, rules)
    for puz in example_puzzles[:n_puzzles]:
        cnf = CNF(puz)
        solve(cnf)

    print("Solved in %s seconds" % (time.time() - start_time))
