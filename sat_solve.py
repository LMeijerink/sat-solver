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
    n_puzzles = 50

    # Load in rules, same for every sudoku
    with open('sudoku-rules.txt') as f:
        rules = f.read()

    example_puzzles = sudokus_to_DIMACS(sudokufile, rules)

    splits_dp = []
    splits_lefv = []
    backtracks_dp = []
    backtracks_lefv = []
    splits = 0
    backtracks = 0

    print("Solving using DP")
    i = 0
    for puz in example_puzzles[:n_puzzles]:
        splits = 0
        backtracks = 0
        print("Puzzle number %d" % i)
        cnf_dp = CNF(puz)
        sudoku_solver = SATSolver(heuristic=None)
        sudoku_solver.solve(cnf_dp)
        splits_dp.append(sudoku_solver.splits)
        backtracks_dp.append(sudoku_solver.backtracks)
        i += 1
    dp_time = time.time() - start_time

    start_time = time.time()
    print("Solving using LEFV")
    i = 0
    for puz in example_puzzles[:n_puzzles]:
        splits = 0
        backtracks = 0
        print("Puzzle number %d" % i)
        cnf_lefv = CNF(puz)
        sudoku_solver = SATSolver(heuristic="LEFV")
        sudoku_solver.solve(cnf_lefv)
        splits_lefv.append(sudoku_solver.splits)
        backtracks_lefv.append(sudoku_solver.backtracks)
        i += 1
    lefv_time = time.time() - start_time

    print("Time taken by DP to solve: %f seconds" % dp_time)
    print("Time taken by LEFV to solve: %f seconds" % lefv_time)
    print("Mean number of splits with DP: ", np.mean(splits_dp))
    print("Mean number of splits with LEFV: ", np.mean(splits_lefv))
    print("Mean number of backtracks with DP: ", np.mean(backtracks_dp))
    print("Mean number of backtracks with LEFV: ", np.mean(backtracks_lefv))
