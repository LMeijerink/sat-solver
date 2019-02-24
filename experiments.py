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


def bin_metrics_by_clues(heuristic, n_puzzles, n_runs, example_puzzles, clues):
    splits_dict = defaultdict(list)
    backtracks_dict = defaultdict(list)

    if heuristic is None:
        print("Solving using DP")
    else:
        print("Solving using %s" % heuristic)

    i = 1
    for (puz, n_clues) in zip(example_puzzles[:n_puzzles], clues[:n_puzzles]):
        print("Puzzle number %d" % i)
        total_splits = 0
        total_backtracks = 0
        for t in range(1, n_runs + 1):
            cnf = CNF(puz)
            sudoku_solver = SATSolver(heuristic=heuristic)
            sudoku_solver.solve(cnf)
            total_splits += sudoku_solver.splits
            total_backtracks += sudoku_solver.backtracks
        splits_dict[n_clues].append(total_splits / float(t))
        backtracks_dict[n_clues].append(total_backtracks / float(t))
        i += 1

    avg_splits_dict = {k: np.mean(splits_dict[k]) for k in splits_dict.keys()}
    avg_backtracks_dict = {k: np.mean(backtracks_dict[k]) for k in backtracks_dict.keys()}
    return avg_splits_dict, avg_backtracks_dict


def plot_splits_backtracks(sudoku_rules_file, sudoku_file, n_puzzles, n_runs):
    width = 0.3
    rules = load_sudoku_rules(sudoku_rules_file)
    example_puzzles, clues = sudokus_to_DIMACS(sudoku_file, rules)

    avg_splits_dp, avg_backtracks_dp = bin_metrics_by_clues(None, n_puzzles, n_runs, example_puzzles, clues)
    avg_splits_lefv, avg_backtracks_lefv = bin_metrics_by_clues('LEFV', n_puzzles, n_runs, example_puzzles, clues)
    avg_splits_up, avg_backtracks_up = bin_metrics_by_clues('UP', n_puzzles, n_runs, example_puzzles, clues)

    N = len(avg_splits_dp)
    ind = np.arange(N)

    fig, ax = plt.subplots()
    ax.bar(ind + width, avg_splits_dp.values(), width, color='r', label='DP')
    ax.bar(ind , avg_splits_up.values(), width, color='y', label='UP')
    ax.bar(ind + 2*width, avg_splits_lefv.values(), width, color='b', label='LEFV')
    
    ax.set_xticks(ind+width)
    ax.set_xticklabels(avg_backtracks_lefv.keys())

    ax.set_xlabel('Number of clues')
    ax.set_ylabel('Average number of splits')
    fig.suptitle('Average number of splits vs number of clues')
    ax.legend()

    fig, ax = plt.subplots()
    ax.bar(ind + width, avg_backtracks_dp.values(), width, color='r', label='DP')
    ax.bar(ind, avg_backtracks_up.values(), width, color='y', label='UP')
    ax.bar(ind+2*width, avg_backtracks_lefv.values(), width, color='b', label='LEFV')
    
    ax.set_xticks(ind+width)

    ax.set_xticklabels(avg_backtracks_lefv.keys())
    ax.set_xlabel('Number of clues')
    ax.set_ylabel('Average number of backtracks')
    fig.suptitle('Average number of backtracks vs number of clues')
    ax.legend()

    plt.show()


if __name__ == '__main__':
    sudoku_rules_file = 'sudoku_rules/sudoku-rules.txt'
    sudoku_file = 'test_sudokus/1000 sudokus.txt'
    n_puzzles = 10
    n_runs = 1

    plot_splits_backtracks(sudoku_rules_file, sudoku_file, n_puzzles, n_runs)
