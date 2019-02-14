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
                vars = map(np.int, line.split()[:-1])
                mask = np.in1d(self.literals, np.abs(vars))
                clause[mask] = np.sign(vars)
                self.clause_matrix[clause_id, :] = clause
                clause_id += 1

    def remove_unit_literals(self):
        literal_count_per_clause = np.sum(self.clause_matrix != 0, axis=1)
        clauses_with_unit_literals = np.where(literal_count_per_clause == 1)[0]
        unit_literal_indices = np.nonzero(self.clause_matrix[clauses_with_unit_literals])[1]
        self.assign[unit_literal_indices] = np.sign(self.clause_matrix[clauses_with_unit_literals, unit_literal_indices])
        self.clause_matrix[clauses_with_unit_literals, unit_literal_indices] = 0
