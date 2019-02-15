from DavisPutnam import DavisPutnam
from cnf import CNF
import numpy as np
import copy

def solve(cnf):
    cnf.simplify()
    if cnf.clauses == []:
        cnf.print_sol()
        return True
    if [] in cnf.clauses:
        return False
    #split
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

# Takes in file of sudokus and returns list of puzzles in DIMACS format
def sudokus_to_DIMACS(filename, rules): 
    puzzles = []
    with open(filename, 'r') as f:
        for line in f.read().splitlines():
            line = np.array(list(line))
            matrix = np.reshape(line, (9, 9))
            clauses = rules
            for x in range(len(matrix)):
                for y in range(len(matrix[x])):
                    if matrix[x,y] != '.':
                        clauses += str(x +1) + str(y+1) + matrix[x,y] + ' 0\n'
            puzzles += [clauses]
    return puzzles
    

sudokufile = '1000 sudokus.txt'

#load in rules, same for every sudoku
with open('sudoku-rules.txt') as f:
    rules = f.read()

example_puzzles = sudokus_to_DIMACS(sudokufile, rules)
for puz in example_puzzles[:10]:
    # cnf = CNF(puz)
    # solve(cnf)
    dp = DavisPutnam(puz)
    dp.solve()
    dp.print_sol()
    # print(dp.clause_matrix)
