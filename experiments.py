import numpy as np
from collections import defaultdict
from sat_solve import sudokus_to_DIMACS
import matplotlib.pyplot as plt
from cnf import CNF
from sat_solve import SATSolver


def load_sudoku_rules(sudoku_rules_file):
    with open(sudoku_rules_file) as f:
        rules = f.read()
    return rules

def get_metrics(heuristic, n_puzzles, n_runs, example_puzzles):
    splits = []
    backtracks = []

    if heuristic is None:
        print("Solving using DP")
    else:
        print("Solving using %s" % heuristic)

    i = 1
    for puz in example_puzzles[:n_puzzles]:
        print("Puzzle number %d" % i)
        total_splits = 0
        total_backtracks = 0
        for t in range(1, n_runs + 1):
            cnf = CNF(puz)
            sudoku_solver = SATSolver(heuristic=heuristic)
            sudoku_solver.solve(cnf)
            total_splits += sudoku_solver.splits
            total_backtracks += sudoku_solver.backtracks
        splits += [total_splits / float(t)]
        backtracks += [total_backtracks / float(t)]
        i += 1

    avg_splits = np.mean(splits)
    avg_backtracks = np.mean(backtracks)
    return avg_splits, avg_backtracks

def plot_metrics(sudoku_file, n_puzzles, n_runs):
    width = 0.3
    xsudoku_rules = load_sudoku_rules('sudoku_rules/xsudoku-rules.txt')
    sudoku_rules = load_sudoku_rules('sudoku_rules/sudoku-rules.txt')

    x_examples, clues = sudokus_to_DIMACS(sudoku_file, xsudoku_rules)
    reg_examples, clues = sudokus_to_DIMACS(sudoku_file, sudoku_rules)

    avg_splits_dp, avg_backtracks_dp,avg_splits_lefv, avg_backtracks_lefv,avg_splits_up, avg_backtracks_up = dict(),dict(),dict(),dict(),dict(),dict()
    
    for examples, label in [(x_examples,'xsudoku'), (reg_examples, 'sudoku')]:
        dp_spl, dp_bt = get_metrics(None, n_puzzles, n_runs, examples)
        avg_splits_dp[label] = dp_spl
        avg_backtracks_dp[label] = dp_bt

        lf_spl, lf_bt = get_metrics("LEFV", n_puzzles, n_runs, examples)
        avg_splits_lefv[label] = lf_spl
        avg_backtracks_lefv[label] = lf_bt

        up_spl, up_bt = get_metrics("UP", n_puzzles, n_runs, examples)
        avg_splits_up[label] = up_spl
        avg_backtracks_up[label] = up_bt

    N = len(avg_splits_dp)
    ind = np.arange(N)

    fig, ax = plt.subplots()

    ax.bar(ind , avg_splits_dp.values(), width, color='r', label='DP')
    ax.bar(ind +width, avg_splits_up.values(), width, color='y', label='UP')
    ax.bar(ind + 2*width, avg_splits_lefv.values(), width, color='b', label='LEFV')
    ax.set_xlabel('Rules')
    ax.set_ylabel('Average number of splits')
    fig.suptitle('Average number of splits vs rules used')
    ax.legend()
    ax.set_xticks(ind+width)
    ax.set_xticklabels(avg_splits_up.keys())

    plt.show()


    fig, ax = plt.subplots()

    ax.bar(ind , avg_backtracks_dp.values(), width, color='r', label='DP')
    ax.bar(ind +width, avg_backtracks_up.values(), width, color='y', label='UP')
    ax.bar(ind + 2*width, avg_backtracks_lefv.values(), width, color='b', label='LEFV')
    ax.set_xlabel('Rules')
    ax.set_ylabel('Average number of backtracks')
    fig.suptitle('Average number of backtracks vs rules used')
    ax.legend()
    ax.set_xticks(ind+width)
    ax.set_xticklabels(avg_splits_up.keys())

    plt.show()


if __name__ == '__main__':
    sudoku_file = 'x_hard.txt'
    n_puzzles = 30
    n_runs = 1

    plot_metrics(sudoku_file, n_puzzles, n_runs)
