import numpy as np
from collections import defaultdict
import copy


class CNF:
    def __init__(self, dimacs_str):
        """
        Class representing a SAT problem in closed normal form
        :param dimacs_str: SAT problem as a DIMACS string
        """
        self.clauses = []  # clauses as lists
        self.assign = defaultdict(int)  # False = -1, True = 1, unassigned = 0
        self.variables = set()
        self.occurences = defaultdict(int)
        self.load_clauses(dimacs_str)
        self.lefv_clause = []
        self.unit_assignments = 0

    def load_clauses(self, dimacs_str):
        """
        Load the clauses into the list from the input DIMACS string
        :param dimacs_str: String in DIMACS format
        :return: None
        """
        for line in dimacs_str.splitlines():
            if line != '' and line[0] != '0' and (line[0] == "-" or line[0].isdigit()):
                clause = []
                for l in line[:-1].split():
                    literal = int(l)
                    if -literal in clause:
                        clause.remove(-literal)  # remove tautology
                    else:
                        clause += [literal]
                    self.variables.add(np.abs(literal))
                    self.occurences[literal] += 1
                self.clauses += [clause]

    def assign_unit_clauses(self):
        """
        Assign value to variables which occur in unit clauses
        :return: True if no conflict and False if a conflict in encountered
        """
        non_unit_clauses = []
        for clause in self.clauses:
            if len(clause) == 1:
                # Conflict encountered
                if np.sign(clause[0]) == -self.assign[np.abs(clause[0])]:
                    return False
                # Otherwise make an assignment
                if self.assign[np.abs(clause[0])] == 0:
                    self.unit_assignments += 1
                self.assign[np.abs(clause[0])] = np.sign(clause[0])
            else:
                non_unit_clauses += [clause]
        self.clauses = non_unit_clauses
        return True

    def assign_pure_literals(self):
        """
        Assign value to variables which are pure literls
        :return: None
        """
        for var in self.variables:
            if self.assign[var] == 0:
                if self.occurences[var] != 0 and self.occurences[-var] == 0:
                    self.assign[var] = 1
                elif self.occurences[-var] != 0 and self.occurences[var] == 0:
                    self.assign[var] = -1

    def rm_redundant_clauses(self):
        """
        Remove redundant clauses and variables based on a new assignment
        :return: None
        """
        unsat_clauses = []
        self.occurences = defaultdict(int)
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
                    self.occurences[var] += 1
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
            if not self.assign_unit_clauses():
                return False
            self.assign_pure_literals()
            self.rm_redundant_clauses()
        return True

    def random_split(self):
        """
        Randomly choose an unassigned variable
        :return: Chosen variable
        """
        variables = [v for v in self.variables if self.assign[v] == 0]
        sgn = np.random.choice([1, -1])
        return sgn*np.random.choice(variables)

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

    def satz(self):
        """
        Choose a variable based on the Satz heuristic
        :return: Chosen variable
        """
        w = defaultdict(int)
        H = defaultdict(int)
        minclauses = self.minclauses()
        for v in self.variables:
            if self.assign[v] == 0:
                if ((self.occurences[v] + self.occurences[-v]) / 2 >= 14 and (
                        self.occurences[v] >= 4 and self.occurences[-v] >= 4)):
                    F1 = copy.deepcopy(self)
                    F2 = copy.deepcopy(self)
                    F1.clauses += [[v]]
                    F2.clauses += [[-v]]
                    F1.simplify()
                    F2.simplify()
                    unsat_F1 = [] in F1.clauses
                    unsat_F2 = [] in F2.clauses
                    if unsat_F1:
                        return -v
                    elif unsat_F2:
                        return v
                    else:
                        w[v] = self.diff(minclauses, F1)
                        w[-v] = self.diff(minclauses, F2)
                        H[v] = w[-v] * w[v] * 1024 + w[-v] + w[v]
                    if len(H) == 5:
                        return max(H.items(), key=lambda l: l[1])[0]

        if len(H) > 0:
            return max(H.items(), key=lambda l: l[1])[0]
        else:
            return self.random_split()

    def minclauses(self):
        minclauses = []
        minlen = float('inf')
        for clause in self.clauses:
            if len(clause) < minlen:
                minlen = len(clause)
                minclauses = [clause]
            if len(clause) == minlen:
                minclauses += [clause]
        return minclauses

    def diff(self, minclauses, other):
        dif = [clause for clause in minclauses if clause not in other.clauses]
        return len(dif)

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
