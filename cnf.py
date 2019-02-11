import numpy as np
from collections import defaultdict

class CNF():
    def __init__(self, dimacs_str):
        self.clauses = []              # clauses as lists
        self.assign = defaultdict(int) # False = -1, True = 1, unassigned = 0 
        self.variables = set()
        self.from_string(dimacs_str)   
        
    def from_string(self, dimacs_str):
        for line in dimacs_str.splitlines():
            if line[0] != "c" and line[0] != "p":
                clause = []
                for v in line[:-1].split():
                    var = int(v)
                    clause += [var]
                    self.variables.add(np.abs(var))
                self.clauses += [clause]

    def unit_literal(self):
        new_clauses = []
        for clause in self.clauses:
            if len(clause) == 1:
                if clause[0] > 0:
                    self.assign[clause[0]] = 1
                else:
                    self.assign[np.abs(clause[0])] = -1
            else:
                new_clauses += [clause]
        self.clauses = new_clauses

    #remove redundant clauses and variables based on a new assignment
    def rm_rd_clauses(self):
        new_clauses = []
        for clause in self.clauses:
            new_vars = []
            sat_clause = False
            for var in clause:
                if self.assign[np.abs(var)]*var > 0:
                    sat_clause = True # so clause does not need to be included
                elif self.assign[np.abs(var)]*var < 0:
                    pass       # false variable so does not need to be included in clause
                else: 
                    new_vars += [var]
            if not sat_clause:
                new_clauses += [new_vars]
        self.clauses = new_clauses
    
    #get new assignments by unit_literal, and remove redundancies, loo
    def simplify(self):
        prev_len = float('inf')
        #simplify
        while len(self.clauses) < prev_len:
            prev_len = len(self.clauses)
            self.unit_literal()
            self.rm_rd_clauses()

    def random_split(self):
        variables = [v for v in self.variables if self.assign[v] == 0]
        return np.random.choice(variables)

    # print solution based on assignments
    def print_sol(self):
        grid = np.zeros((9,9))
        for key in self.assign.keys():
            if self.assign[key] == 1:
                x, y = str(key)[0], str(key)[1]
                grid[int(x) -1,int(y) -1] = str(key)[2]
        print(grid)