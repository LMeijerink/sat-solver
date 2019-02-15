import numpy as np


class DavisPutnam():

    def __init__(self, dimacs_str):
        self.literals = set()
        self.n_clauses = 0
        for line in dimacs_str.splitlines():
            if line[0] != "c" and line[0] != "p":
                for v in line[:-1].split():
                    var = int(v)
                    self.literals.add(np.abs(var))
                self.n_clauses += 1
        self.literals = np.array(list(self.literals))
        self.clause_matrix = np.zeros((self.n_clauses, len(self.literals)), dtype=int)
        self.assign = np.zeros(len(self.literals), dtype=int)
        clause_id = 0
        for line in dimacs_str.splitlines():
            if line[0] != "c" and line[0] != "p":
                clause = np.zeros(len(self.literals), dtype=int)
                variables = list(map(np.int, line.split()[:-1]))
                mask = np.in1d(self.literals, np.abs(variables))
                clause[mask] = np.sign(variables)
                self.clause_matrix[clause_id, :] = clause
                clause_id += 1

    def simplify_unit_clauses(self):
        literal_count_per_clause = np.sum(self.clause_matrix != 0, axis=1)
        clauses_with_unit_literals = np.where(literal_count_per_clause == 1)[0]
        pos_literal_indices = np.where(self.clause_matrix[clauses_with_unit_literals, :] == 1)[1]
        self.assign[pos_literal_indices] = 1
        self.clause_matrix[:, pos_literal_indices] = 0
        neg_literal_indices = np.where(self.clause_matrix[clauses_with_unit_literals, :] == -1)[1]
        self.assign[neg_literal_indices] = -1
        clauses_to_remove = np.where(self.clause_matrix[:, pos_literal_indices] == 1)[0]
        self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0)
        clauses_to_remove = np.where(self.clause_matrix[:, neg_literal_indices] == -1)[0]
        self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0)
        self.clause_matrix[:, neg_literal_indices] = 0

    def simplify_pure_literals(self):
        pos_literal_indices = np.all(self.clause_matrix >= 0, axis=0)
        self.assign[pos_literal_indices] = 1
        clauses_to_remove = np.where(self.clause_matrix[:, pos_literal_indices] == 1)[0]
        self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0)
        neg_literal_indices = np.all(self.clause_matrix <= 0, axis=0)
        self.assign[neg_literal_indices] = -1
        clauses_to_remove = np.where(self.clause_matrix[:, neg_literal_indices] == -1)[0]
        self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0)

    def choose_literal(self):
        return np.random.choice(np.where(self.assign == 0)[0])

    def solve(self):
        # self.simplify_unit_clauses()
        # self.simplify_pure_literals()
        if self.clause_matrix.shape[0] == 0:
            return True
        if np.sum(np.all(self.clause_matrix == 0, axis=1)) > 0:
            return False
        s = self.choose_literal()
        clause_state = np.array(self.clause_matrix)
        assign_state = np.array(self.assign)
        self.assign[s] = 1
        clauses_to_remove = np.where(self.clause_matrix[:, s] == 1)[0]  # eliminate clauses with positive occurrences
        self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0)
        self.clause_matrix[:, s] = 0  # eliminate negative occurrences
        if self.solve() == False:
            self.clause_matrix = np.array(clause_state)
            self.assign = np.array(assign_state)
            self.assign[s] = -1
            clauses_to_remove = np.where(self.clause_matrix[:, s] == -1)[0]
            self.clause_matrix = np.delete(self.clause_matrix, clauses_to_remove, axis=0) # eliminate clauses with negative occurrences
            self.clause_matrix[:, s] = 0 # eliminate positive occurrences
            return self.solve()
        return True

    # print solution based on assignments
    def print_sol(self):
        grid = np.zeros((9, 9))
        for (i, key) in enumerate(self.literals):
            if self.assign[i] == 1:
                x, y = str(key)[0], str(key)[1]
                grid[int(x) - 1, int(y) - 1] = str(key)[2]
        print(grid)