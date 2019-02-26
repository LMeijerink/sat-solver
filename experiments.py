import numpy as np
import matplotlib.pyplot as plt
from cnf import CNF
from sat_solve import SATSolver


def load_sudoku_rules(sudoku_rules_file):
    with open(sudoku_rules_file) as f:
        rules = f.read()
    return rules


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


def get_metrics(heuristic, n_puzzles, n_runs, example_puzzles):
    splits = []
    backtracks = []
    unit_assigns = []

    if heuristic is None:
        print("Solving using DP")
    else:
        print("Solving using %s" % heuristic)

    i = 1
    for puz in example_puzzles[:n_puzzles]:
        print("Puzzle number %d" % i)
        total_splits = 0
        total_backtracks = 0
        total_unit_assigns = 0
        for t in range(1, n_runs + 1):
            cnf = CNF(puz)
            sudoku_solver = SATSolver(heuristic=heuristic)
            sudoku_solver.solve(cnf)
            total_splits += sudoku_solver.splits
            total_backtracks += sudoku_solver.backtracks
            total_unit_assigns += cnf.unit_assignments
        splits += [total_splits / float(t)]
        backtracks += [total_backtracks / float(t)]
        unit_assigns += [total_unit_assigns / float(t)]
        i += 1

    avg_splits = np.mean(splits)
    avg_backtracks = np.mean(backtracks)
    avg_unit_assigns = np.mean(unit_assigns)
    standarddeviations = np.std(splits)/2, np.std(backtracks)/2, np.std(unit_assigns)/2

    return avg_splits, avg_backtracks, avg_unit_assigns/avg_splits, standarddeviations


def plot_metrics(sudoku_file, n_puzzles, n_runs):
    width = 0.3
    xsudoku_rules = load_sudoku_rules('sudoku_rules/xsudoku-rules.txt')
    sudoku_rules = load_sudoku_rules('sudoku_rules/sudoku-rules.txt')

    x_examples, clues = sudokus_to_DIMACS(sudoku_file, xsudoku_rules)
    reg_examples, clues = sudokus_to_DIMACS(sudoku_file, sudoku_rules)

    avg_splits_dp, avg_backtracks_dp, avg_splits_lefv, avg_backtracks_lefv, avg_splits_up, avg_backtracks_up = dict(), dict(), dict(), dict(), dict(), dict()
    avg_unit_assigns_dp, avg_unit_assigns_lefv, avg_unit_assigns_up = dict(), dict(), dict()
    dp_stds, lf_stds, up_stds = dict(), dict(), dict()
    for examples, label in [(x_examples, 'xsudoku'), (reg_examples, 'sudoku')]:
        dp_spl, dp_bt, dp_ua, dp_std = get_metrics(None, n_puzzles, n_runs, examples)
        avg_splits_dp[label] = dp_spl
        avg_backtracks_dp[label] = dp_bt
        avg_unit_assigns_dp[label] = dp_ua
        dp_stds[label] = dp_std

        lf_spl, lf_bt, lf_ua, lf_std = get_metrics("LEFV", n_puzzles, n_runs, examples)
        avg_splits_lefv[label] = lf_spl
        avg_backtracks_lefv[label] = lf_bt
        avg_unit_assigns_lefv[label] = lf_ua
        lf_stds[label] = lf_std

        up_spl, up_bt, up_ua, up_std = get_metrics("UP", n_puzzles, n_runs, examples)
        avg_splits_up[label] = up_spl
        avg_backtracks_up[label] = up_bt
        avg_unit_assigns_up[label] = up_ua
        up_stds[label] = up_std

    N = len(avg_splits_dp)
    ind = np.arange(N)

    fig, ax = plt.subplots()

    ax.bar(ind, avg_splits_dp.values(), width, yerr= [dp_stds['xsudoku'][0], dp_stds['sudoku'][0]], color='r', label='DP')
    ax.bar(ind + width, avg_splits_up.values(), width, yerr= [up_stds['xsudoku'][0], up_stds['sudoku'][0]],  color='y', label='UP')
    ax.bar(ind + 2 * width, avg_splits_lefv.values(), width, yerr= [lf_stds['xsudoku'][0], lf_stds['sudoku'][0]], color='b', label='LEFV')
    ax.set_xlabel('Rules')
    ax.set_ylabel('Average number of splits')
    fig.suptitle('Average number of splits for Sudoku and X-Sudoku')
    ax.legend()
    ax.set_xticks(ind + width)
    ax.set_xticklabels(avg_splits_dp.keys())

    fig, ax = plt.subplots()

    ax.bar(ind, avg_backtracks_dp.values(), width, yerr= [dp_stds['xsudoku'][1], dp_stds['sudoku'][1]], color='r', label='DP')
    ax.bar(ind + width, avg_backtracks_up.values(), width, yerr= [up_stds['xsudoku'][1], up_stds['sudoku'][1]], color='y', label='UP')
    ax.bar(ind + 2 * width, avg_backtracks_lefv.values(), width, yerr= [lf_stds['xsudoku'][1], lf_stds['sudoku'][1]], color='b', label='LEFV')
    ax.set_xlabel('Rules')
    ax.set_ylabel('Average number of backtracks')
    fig.suptitle('Average number of backtracks for Sudoku and X-Sudoku')
    ax.legend()
    ax.set_xticks(ind + width)
    ax.set_xticklabels(avg_splits_up.keys())

    fig, ax = plt.subplots()
    ax.bar(ind, avg_unit_assigns_dp.values(), width, yerr= [dp_stds['xsudoku'][2], dp_stds['sudoku'][2]], color='r', label='DP')
    ax.bar(ind + width, avg_unit_assigns_up.values(), width, yerr= [up_stds['xsudoku'][2], up_stds['sudoku'][2]], color='y', label='UP')
    ax.bar(ind + 2 * width, avg_unit_assigns_lefv.values(), width, yerr= [lf_stds['xsudoku'][2], lf_stds['sudoku'][2]], color='b', label='LEFV')
    ax.set_xlabel('Rules')
    ax.set_ylabel('Average number of unit assignments per split')
    fig.suptitle('Average number of unit assignments per split for Sudoku and X-Sudoku')
    ax.legend()
    ax.set_xticks(ind + width)
    ax.set_xticklabels(avg_splits_up.keys())

    plt.show()


if __name__ == '__main__':
    sudoku_file = 'test_sudokus/xsudoku_hard.txt'
    n_puzzles = 30
    n_runs = 1

    plot_metrics(sudoku_file, n_puzzles, n_runs)
