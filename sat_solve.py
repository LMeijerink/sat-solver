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
        elif self.heuristic == 'UP':
            s = cnf.satz()
        self.splits += 1
        cnf1 = copy.deepcopy(cnf)
        cnf1.clauses += [[s]]
        if self.solve(cnf1):
            cnf.assign = cnf1.assign
            cnf.clauses = cnf1.clauses
            cnf.unit_assignments = cnf1.unit_assignments - 1
            return True
        else:
            cnf.unit_assignments = cnf1.unit_assignments - 1
            self.backtracks += 1
            cnf2 = copy.deepcopy(cnf)
            cnf2.clauses += [[-s]]
            if self.solve(cnf2):
                cnf.assign = cnf2.assign
                cnf.clauses = cnf2.clauses
                cnf.unit_assignments = cnf2.unit_assignments - 1
                return True
            cnf.unit_assignments = cnf2.unit_assignments - 1
        return False

