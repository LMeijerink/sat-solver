import numpy as np
from collections import defaultdict


class CNF:
    def __init__(self, dimacs_str):
        """
        Class representing a SAT problem in closed normal form
        :param dimacs_str: SAT problem as a DIMACS string
        """
        self.clauses = []  # clauses as lists
        self.assign = defaultdict(int)  # False = -1, True = 1, unassigned = 0
        self.variables = set()
        self.load_clauses(dimacs_str)
        self.lefv_clause = []

    def load_clauses(self, dimacs_str):
        """
        Load the clauses into the list from the input DIMACS string
        :param dimacs_str: String in DIMACS format
        :return: None
        """
        for line in dimacs_str.splitlines():
            if line[0] != "c" and line[0] != "p":
                clause = []
                for l in line[:-1].split():
                    literal = int(l)
                    if -literal in clause:
                        clause.remove(-literal)  # remove tautology
                    else:
                        clause += [literal]
                    self.variables.add(np.abs(literal))
                self.clauses += [clause]

    def assign_unit_clauses(self):
        """
        Assign value to variables which occur in unit clauses
        :return: None
        """
        non_unit_clauses = []
        for clause in self.clauses:
            if len(clause) == 1:
                self.assign[np.abs(clause[0])] = np.sign(clause[0])
            else:
                non_unit_clauses += [clause]
        self.clauses = non_unit_clauses

    def assign_pure_literals(self):
        """
        Assign value to variables which are pure literls
        :return: None
        """
        literal_count = defaultdict(int)
        for clause in self.clauses:
            for literal in clause:
                literal_count[literal] += 1
        for var in self.variables:
            if self.assign[var] == 0:
                if literal_count[var] != 0 and literal_count[-var] == 0:
                    self.assign[var] = 1
                elif literal_count[-var] != 0 and literal_count[var] == 0:
                    self.assign[var] = -1

    def rm_redundant_clauses(self):
        """
        Remove redundant clauses and variables based on a new assignment
        :return: None
        """
        unsat_clauses = []
        for clause in self.clauses:
            unassigned_vars = []
            sat_clause = False
            clause_with_elim_variable = False
            for var in clause:
                if self.assign[np.abs(var)] * var > 0:
                    sat_clause = True  # so clause does not need to be included
                elif self.assign[np.abs(var)] * var < 0:
                    # false variable so does not need to be included in clause
                    clause_with_elim_variable = True
                else:
                    unassigned_vars += [var]
            if not sat_clause:
                unsat_clauses += [unassigned_vars]
                if clause_with_elim_variable:
                    self.lefv_clause = list(clause)
        self.clauses = unsat_clauses

    def simplify(self):
        """
        Assign variables in unit clauses and remove redundant clauses
        :return: None
        """
        prev_len = float('inf')
        while len(self.clauses) < prev_len:
            prev_len = len(self.clauses)
            self.assign_unit_clauses()
            self.assign_pure_literals()
            self.rm_redundant_clauses()

    def random_split(self):
        """
        Randomly choose an unassigned variable
        :return: Chosen variable
        """
        variables = [v for v in self.variables if self.assign[v] == 0]
        return np.random.choice(variables)

    def lefv_split(self):
        """
        Choose a free variable from the last encountered unsatisfied clause during unit propagation
        :return: Chosen variable
        """
        lefvs = [v for v in self.lefv_clause if self.assign[np.abs(v)] == 0]
        if len(lefvs) != 0:
            return np.random.choice(lefvs)
        else:
            variables = [v for v in self.variables if self.assign[v] == 0]
            return np.random.choice(variables)

    def print_sol(self):
        """
        Print sudoku solution as a matrix
        :return: None
        """
        grid = np.zeros((9, 9))
        for key in self.assign.keys():
            if self.assign[key] == 1:
                x, y = str(key)[0], str(key)[1]
                grid[int(x) - 1, int(y) - 1] = str(key)[2]
        print(grid)
