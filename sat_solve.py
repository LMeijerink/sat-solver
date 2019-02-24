import time
from cnf import CNF
import numpy as np
import copy


class SATSolver:

    def __init__(self, heuristic=None):
        """
        SAT solver
        :param heuristic: Heuristic to use for solving. Empty for vanilla Davis Putnam
        """
        self.splits = 0
        self.backtracks = 0
        self.heuristic = heuristic

    def solve(self, cnf):
        """
        Solve a SAT problem
        :param cnf: Object containing the problem in closed normal form
        :return: True if solvable else False
        """
        if not cnf.simplify():
            return False
        if cnf.clauses == []:
            # cnf.print_sol()
            return True
        if [] in cnf.clauses:
            return False
        # Split
        if self.heuristic is None:
            s = cnf.random_split()
        elif self.heuristic == 'LEFV':
            s = cnf.lefv_split()
        elif self.heuristic == 'UP':
            s = cnf.satz()
        self.splits += 1
        cnf1 = copy.deepcopy(cnf)
        cnf1.clauses += [[s]]
        if self.solve(cnf1):
            cnf.assign = cnf1.assign
            cnf.clauses = cnf1.clauses
            return True
        else:
            self.backtracks += 1
            cnf2 = copy.deepcopy(cnf)
            cnf2.clauses += [[-s]]
            if self.solve(cnf2):
                cnf.assign = cnf2.assign
                cnf.clauses = cnf2.clauses
                return True
        return False


def sudokus_to_DIMACS(filename, rules):
    """
    Takes in file of sudokus and returns a list of puzzles in DIMACS format
    :param filename: Filename of sudoku problems
    :param rules: String of sudoku rules
    :return: String containing rules and sudoku problems in DIMACS format, and the number of clues in each problem
    """
    puzzles = []
    n_clues = []
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            line = np.array(list(line))
            matrix = np.reshape(line, (9, 9))
            clauses = rules
            clues = 0
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if matrix[x, y] != '.':
                        clauses += str(x + 1) + str(y + 1) + matrix[x, y] + ' 0\n'
                        clues += 1
            puzzles += [clauses]
            n_clues.append(clues)
    return puzzles, n_clues


if __name__ == '__main__':
    sudokufile = 'test_sudokus/1000 sudokus.txt'
    n_puzzles = 30
    n_runs = 5

    # Load in rules, same for every sudoku
    with open('sudoku-rules.txt') as f:
        rules = f.read()

    example_puzzles, clues = sudokus_to_DIMACS(sudokufile, rules)

    pass
