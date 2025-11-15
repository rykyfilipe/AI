"""Date comune folosite în aplicație: cursuri, sinonime și șabloane de întrebări."""

cursuri = {
    "C1: Search Problems": {
        "n-queens": {
            "descriere": "Problema de a plasa N regine pe o tablă de șah",
            "strategii": ["backtracking", "local search", "constraint satisfaction"],
            "optimizari": ["MRV", "FC", "AC-3"],
        },
        "knight_tour": {
            "descriere": "Problema călărețului - parcurgerea tuturor pătratelor unei table",
            "strategii": ["backtracking", "heuristic search", "depth first search"],
            "optimizari": ["Warnsdorff heuristic", "pruning"],
        },
        "hanoi": {
            "descriere": "Problema Turnurilor din Hanoi",
            "strategii": ["recursion", "dynamic programming", "iterative"],
            "optimizari": ["memoization"],
        },
    },
    "C2: Constraint Satisfaction": {
        "graph_coloring": {
            "descriere": "Colorarea unui graf cu numărul minim de culori",
            "strategii": ["backtracking", "constraint satisfaction", "greedy"],
            "optimizari": ["AC-3", "MRV", "FC"],
        },
        "sudoku": {
            "descriere": "Problema de completare a unui puzzle sudoku",
            "strategii": ["backtracking", "constraint propagation", "AC-3"],
            "optimizari": ["AC-3", "MRV", "forward checking"],
        },
    },
    "C3: Game Theory": {
        "nash_equilibrium": {
            "descriere": "Echilibrul Nash într-un joc în formă normală",
            "strategii": ["dominance elimination", "best response", "mixed strategy"],
            "optimizari": [],
            "generative_functions": [] #list of the functions that this problem can use to generate a game
        },
        "minmax_alphabeta": {
            "descriere": "Strategia MinMax cu optimizarea Alpha-Beta",
            "strategii": ["minimax", "alpha-beta pruning", "iterative deepening"],
            "optimizari": ["alpha-beta pruning", "transposition tables"],
        },
    },
    "C5: Game Theory": {

    }
}

sinonime = {
    "n-queens": ["n-queens", "nqueens", "regine", "8 regine"],
    "knight_tour": ["knight tour", "knight's tour", "cavaler", "calaret"],
    "hanoi": ["hanoi", "turnuri"],
    "graph_coloring": ["graph coloring", "colorare graf", "coloring"],
    "sudoku": ["sudoku"],
    "nash_equilibrium": ["nash", "equilibrium", "echilibru"],
    "minmax_alphabeta": ["minmax", "alpha-beta", "alphabeta", "game tree"],
    "C1: Search Problems": ["c1", "search", "problems"],
    "C2: Constraint Satisfaction": ["c2", "constraint", "satisfaction", "csp"],
    "C3: Game Theory": ["c3", "game theory", "game"],
}

sabloane_intrebari = [
    "Pentru problema {problema}, care este cea mai potrivită strategie dintre următoarele: {strategii}?",
    "Explicați de ce {strategie} este cea mai bună alegere pentru {problema}.",
    "Pentru {problema} rezolvată cu {strategie}, ce optimizare este cea mai eficientă: {optimizari}?",
    "Care sunt avantajele și dezavantajele utilizării {strategie} pentru {problema}?",
    "Care va fi asignarea variabilelor rămase date fiind variabilele, domeniile, constrângerile și asignarea parțială, dacă am utiliza Backtracking cu optimizarea (FC, MRV sau AC-3) pentru continuarea rezolvării?",
    "Pentru jocul dat în forma normală: {joc}, există echilibru Nash pur?",
    "Pentru arborele dat, care va fi valoarea din rădăcină și câte noduri frunze vor fi vizitate cu MinMax + Alpha-Beta?",
    "Cum diferă {strategie} de alte strategii în rezolvarea {problema}?",
    "Ce complexitate în timp și spațiu are {strategie} pentru {problema}?",
]
