import re

cursuri = {
    "C1: Search Problems": {
        "n-queens": {
            "descriere": "Problema de a plasa N regine pe o tablă de șah",
            "strategii": ["backtracking", "local search", "constraint satisfaction"],
            "optimizari": ["MRV", "FC", "AC-3"]
        },
        "knight_tour": {
            "descriere": "Problema călărețului - parcurgerea tuturor pătratelor unei table",
            "strategii": ["backtracking", "heuristic search", "depth first search"],
            "optimizari": ["Warnsdorff heuristic", "pruning"]
        },
        "hanoi": {
            "descriere": "Problema Turnurilor din Hanoi",
            "strategii": ["recursion", "dynamic programming", "iterative"],
            "optimizari": ["memoization"]
        }
    },
    "C2: Constraint Satisfaction": {
        "graph_coloring": {
            "descriere": "Colorarea unui graf cu numărul minim de culori",
            "strategii": ["backtracking", "constraint satisfaction", "greedy"],
            "optimizari": ["AC-3", "MRV", "FC"]
        },
        "sudoku": {
            "descriere": "Problema de completare a unui puzzle sudoku",
            "strategii": ["backtracking", "constraint propagation", "AC-3"],
            "optimizari": ["AC-3", "MRV", "forward checking"]
        }
    },
    "C3: Game Theory": {
        "nash_equilibrium": {
            "descriere": "Echilibrul Nash într-un joc în formă normală",
            "strategii": ["dominance elimination", "best response", "mixed strategy"],
            "optimizari": []
        },
        "minmax_alphabeta": {
            "descriere": "Strategia MinMax cu optimizarea Alpha-Beta",
            "strategii": ["minimax", "alpha-beta pruning", "iterative deepening"],
            "optimizari": ["alpha-beta pruning", "transposition tables"]
        }
    }
}

class EvaluatorRaspunsuri:
    @staticmethod
    def normalize(text):
        return text.lower().replace("ă", "a").replace("î", "i").replace("ș","s").replace("ț","t")

    def verifica(self, intrebare, raspuns, problema, info):
        intrebare_n = self.normalize(intrebare)
        raspuns_n = self.normalize(raspuns)

        scor = 0
        feedback = []

        # verificare strategie
        strategii = [self.normalize(s) for s in info["strategii"]]
        if any(s in raspuns_n for s in strategii):
            scor += 40
        else:
            feedback.append("Nu ai menționat o strategie corectă.")

        # verificare optimizari daca sunt cerute
        if "optimiz" in intrebare_n and info["optimizari"]:
            optimizari = [self.normalize(o) for o in info["optimizari"]]
            if any(o in raspuns_n for o in optimizari):
                scor += 30
            else:
                feedback.append("Nu ai menționat optimizările specifice problemei.")

        # verificare daca raspunde la conceptul intrebarii
        if any(kw in raspuns_n for kw in ["complexitate","timp","spatiu","o(n)", "mai rapid", "mai lent"]):
            scor += 20

        if any(kw in intrebare_n for kw in ["de ce", "avantaje"]):
            if any(kw in raspuns_n for kw in ["eficient", "rapid", "reduce","optimal","garanteaza","mai bun"]):
                scor += 20

        # bonus daca apare descrierea problemei
        if info["descriere"].split()[0].lower() in raspuns_n:
            scor += 10

        if scor > 100:
            scor = 100

        if scor < 60:
            feedback.insert(0, "Răspuns incomplet sau incorect.")
        else:
            feedback.insert(0, "Răspuns corect.")

        return {
            "scor": scor,
            "feedback": " ".join(feedback) if feedback else "Foarte bine!"
        }

eval = EvaluatorRaspunsuri()
info = cursuri["C1: Search Problems"]["n-queens"]

rez = eval.verifica(
    intrebare="De ce este backtracking o strategie buna pentru n-queens?",
    raspuns="Backtracking garanteaza solutia si exploreaza configuratiile eficiente.",
    problema="n-queens",
    info=info
)

print(rez)
