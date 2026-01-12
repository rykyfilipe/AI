from collections import deque
from copy import deepcopy


# =========================
# STRUCTURA CSP
# =========================

class CSP:
    def __init__(self, variables, domains, constraints):
        """
        variables   = list[str]
        domains     = dict[var] -> list[valori]
        constraints = dict[(X,Y)] -> functie(X_val, Y_val) -> bool
        """
        self.variables = variables
        self.domains = deepcopy(domains)
        self.constraints = constraints


# =========================
# UTILITARE
# =========================

def consistent(var, value, assignment, csp):
    """Verifică dacă (var=value) este compatibil cu asignarea curentă"""
    for v in assignment:
        if (var, v) in csp.constraints:
            if not csp.constraints[(var, v)](value, assignment[v]):
                return False
        if (v, var) in csp.constraints:
            if not csp.constraints[(v, var)](assignment[v], value):
                return False
    return True


# =========================
# MRV – alegere variabilă
# =========================

def select_unassigned_variable(assignment, csp):
    """MRV heuristic"""
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda v: len(csp.domains[v]))


# =========================
# FORWARD CHECKING
# =========================

def forward_check(var, value, csp, assignment):
    """Elimină valorile imposibile din domeniile vecinilor"""
    removed = {}

    for v in csp.variables:
        if v not in assignment and v != var:
            key1 = (var, v)
            key2 = (v, var)

            if key1 in csp.constraints or key2 in csp.constraints:
                removed[v] = []
                for val in csp.domains[v][:]:
                    ok = True
                    if key1 in csp.constraints:
                        ok = csp.constraints[key1](value, val)
                    if key2 in csp.constraints:
                        ok = csp.constraints[key2](val, value)

                    if not ok:
                        csp.domains[v].remove(val)
                        removed[v].append(val)

                if not csp.domains[v]:
                    return False, removed

    return True, removed


def restore_domains(csp, removed):
    for v, vals in removed.items():
        csp.domains[v].extend(vals)


# =========================
# AC-3
# =========================

def revise(csp, xi, xj):
    revised = False
    for x in csp.domains[xi][:]:
        ok = False
        for y in csp.domains[xj]:
            if (xi, xj) in csp.constraints:
                if csp.constraints[(xi, xj)](x, y):
                    ok = True
            else:
                ok = True

        if not ok:
            csp.domains[xi].remove(x)
            revised = True
    return revised


def ac3(csp):
    queue = deque(csp.constraints.keys())

    while queue:
        (xi, xj) = queue.popleft()
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for (xk, _) in csp.constraints:
                if xk != xj:
                    queue.append((xk, xi))
    return True


# =========================
# BACKTRACKING CU OPTIMIZĂRI
# =========================

def backtracking_search(csp, assignment,
                        use_mrv=True,
                        use_fc=False,
                        use_ac3=False):
    """Returnează asignarea completă"""

    # dacă am terminat
    if len(assignment) == len(csp.variables):
        return assignment

    # selectare variabilă
    if use_mrv:
        var = select_unassigned_variable(assignment, csp)
    else:
        var = next(v for v in csp.variables if v not in assignment)

    for value in csp.domains[var]:
        if consistent(var, value, assignment, csp):

            assignment[var] = value
            domains_backup = deepcopy(csp.domains)

            # FC
            if use_fc:
                ok, removed = forward_check(var, value, csp, assignment)
                if not ok:
                    del assignment[var]
                    restore_domains(csp, removed)
                    continue

            # AC-3
            if use_ac3:
                if not ac3(csp):
                    del assignment[var]
                    csp.domains = domains_backup
                    continue

            result = backtracking_search(
                csp, assignment,
                use_mrv, use_fc, use_ac3
            )

            if result:
                return result

            del assignment[var]
            csp.domains = domains_backup

    return None


# =========================
# API PRINCIPALĂ
# =========================

def solve_from_partial_assignment(variables,
                                  domains,
                                  constraints,
                                  partial_assignment,
                                  method="FC"):
    """
    method = "BT" | "FC" | "MRV" | "AC3"
    """

    csp = CSP(variables, domains, constraints)

    assignment = dict(partial_assignment)

    use_mrv = method in ["MRV", "FC", "AC3"]
    use_fc  = method in ["FC", "AC3"]
    use_ac3 = method == "AC3"

    solution = backtracking_search(
        csp,
        assignment,
        use_mrv=use_mrv,
        use_fc=use_fc,
        use_ac3=use_ac3
    )

    return solution
