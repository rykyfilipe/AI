import itertools
import random
import math
import re
from typing import List, Dict, Any, Tuple

# ==========================================
# 1. KNOWLEDGE BASE (Romanian Content)
# ==========================================
KNOWLEDGE_BASE = {
    "C1: Search Problems": {
        "n-queens": {
            "description": "Problema de a plasa N regine pe o tabla de sah astfel incat sa nu se atace.",
            "strategies": ["backtracking", "local search (min-conflicts)", "genetic algorithms"],
            "optimizations": ["MRV (Minimum Remaining Values)", "Forward Checking"],
            "type": "search_strategy"
        },
        "knight_tour": {
            "description": "Problema calaretului - parcurgerea tuturor patratelor unei table o singura data.",
            "strategies": ["backtracking", "Warnsdorff's rule"],
            "optimizations": ["pruning"],
            "type": "search_strategy"
        }
    },
    "C2: Constraint Satisfaction": {
        "graph_coloring": {
            "description": "Colorarea unui graf cu numarul minim de culori astfel incat nodurile adiacente sa aiba culori diferite.",
            "strategies": ["backtracking", "constraint satisfaction", "greedy coloring"],
            "optimizations": ["MRV", "Forward Checking", "AC-3"],
            "type": "csp"
        },
        "hanoi": {
            "description": "Problema Turnurilor din Hanoi - mutarea unui stack de discuri de diferite marimi intre tije.",
            "strategies": ["recursion", "dynamic programming", "backtracking"],
            "optimizations": ["memoization"],
            "type": "search_strategy"
        }
    },
    "C3: Game Theory": {
        "nash_equilibrium": {
            "description": "Situatia in care niciun jucator nu castiga schimbandu-si strategia unilateral.",
            "strategies": ["dominance elimination", "best response"],
            "optimizations": [],
            "type": "matrix_game"
        },
        "minmax_alphabeta": {
            "description": "Algoritm pentru jocuri cu suma nula, folosind taierea ramurilor inutile.",
            "strategies": ["minimax", "alpha-beta pruning"],
            "optimizations": ["move ordering", "transposition tables"],
            "type": "tree_game"
        }
    }
}

SYNONYMS = {
    "n-queens": ["n-queens", "regine"],
    "knight_tour": ["knight tour", "calarel", "calaret"],
    "graph_coloring": ["graph coloring", "colorare graf", "coloring", "colorare"],
    "hanoi": ["hanoi", "turnuri"],
    "nash_equilibrium": ["nash", "echilibru"],
    "minmax_alphabeta": ["minmax", "alpha-beta", "arbore", "tree"],
}


# ==========================================
# 2. DOMAIN LOGIC (Solvers & Generators)
# ==========================================

class Node:
    """Represents a node in the Game Tree."""

    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

    def is_leaf(self):
        return len(self.children) == 0


class GameEngine:
    """Handles the math/logic: Tree generation, Nash solving, Minimax."""

    @staticmethod
    def generate_random_tree(depth, branching_factor, min_val=1, max_val=20):
        if depth == 0:
            return Node(value=random.randint(min_val, max_val))
        node = Node()
        for _ in range(branching_factor):
            node.children.append(GameEngine.generate_random_tree(depth - 1, branching_factor, min_val, max_val))
        return node

    @staticmethod
    def tree_to_ascii(node, prefix="", is_last=True, is_max=True, accumulator=None):
        """Creates a string representation of the tree."""
        if accumulator is None:
            accumulator = []

        connector = "└── " if is_last else "├── "
        label = f"({node.value})" if node.is_leaf() else ("MAX" if is_max else "MIN")
        accumulator.append(f"{prefix}{connector}{label}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            GameEngine.tree_to_ascii(child, child_prefix, is_last_child, not is_max, accumulator)

        return "\n".join(accumulator)

    @staticmethod
    def solve_alpha_beta(root_node):
        """Returns (root_value, visited_leaves_count)."""
        visited_leaves = 0

        def alpha_beta(node, alpha, beta, is_max):
            nonlocal visited_leaves
            if node.is_leaf():
                visited_leaves += 1
                return node.value

            if is_max:
                v = -math.inf
                for child in node.children:
                    v = max(v, alpha_beta(child, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha: break
                return v
            else:
                v = math.inf
                for child in node.children:
                    v = min(v, alpha_beta(child, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha: break
                return v

        val = alpha_beta(root_node, -math.inf, math.inf, True)
        return val, visited_leaves

    # @staticmethod
    # def generate_nash_matrix(rows=2, cols=2):
    #     return [[(random.randint(0, 9), random.randint(0, 9)) for _ in range(cols)] for _ in range(rows)]
    #
    # @staticmethod
    # def format_matrix(matrix):
    #     return "[\n" + ",\n".join([str(row) for row in matrix]) + "\n]"
    #
    # @staticmethod
    # def solve_nash(matrix):
    #     rows = len(matrix)
    #     cols = len(matrix[0])
    #     equilibria = []
    #
    #     # Find Best Response for P1 (Row player matches Row index)
    #     best_r = {c: [] for c in range(cols)}
    #     for c in range(cols):
    #         max_val = max(matrix[r][c][0] for r in range(rows))
    #         for r in range(rows):
    #             if matrix[r][c][0] == max_val: best_r[c].append(r)
    #
    #     # Find Best Response for P2 (Col player matches Col index)
    #     best_c = {r: [] for r in range(rows)}
    #     for r in range(rows):
    #         max_val = max(matrix[r][c][1] for c in range(cols))
    #         for c in range(cols):
    #             if matrix[r][c][1] == max_val: best_c[r].append(c)
    #
    #     # Intersection
    #     for r in range(rows):
    #         for c in range(cols):
    #             if r in best_r[c] and c in best_c[r]:
    #                 equilibria.append(f"(Row {r}, Col {c}) -> Payoffs {matrix[r][c]}")
    #
    #     return equilibria if equilibria else ["Niciun echilibru Nash pur"]

    @staticmethod
    def generate_n_player_game(num_players=3, strategies_per_player=2):
        """
        Generează o structură de joc pentru N jucători.
        Returnează:
          - payoffs: Dict {(s1, s2, ...): (payoff1, payoff2, ...)}
          - ranges: Lista cu numărul de strategii pt fiecare jucător [2, 2, 2]
        """
        # Definim câte strategii are fiecare jucător (presupunem egal pentru simplitate)
        ranges = [range(strategies_per_player) for _ in range(num_players)]

        payoffs = {}
        # Generăm produsul cartezian al tuturor strategiilor (ex: (0,0,0), (0,0,1)...)
        all_profiles = itertools.product(*ranges)

        for profile in all_profiles:
            # Generăm payoff-uri random pentru fiecare jucător în acest profil
            payoff_tuple = tuple(random.randint(0, 9) for _ in range(num_players))
            payoffs[profile] = payoff_tuple

        return payoffs, strategies_per_player

    @staticmethod
    def format_n_player_game(payoffs, num_players):
        """Afișează jocul sub formă de listă (matricea e imposibil de desenat pt N>2)."""
        output = [f"Joc cu {num_players} jucători. Payoffs (J1, J2, ...):"]
        for profile, scores in payoffs.items():
            strat_str = ", ".join([f"S{i}" for i in profile])
            output.append(f"  Strategii [{strat_str}] -> Payoffs {scores}")
        return "\n".join(output)

    @staticmethod
    def solve_n_player_nash(payoffs, num_players, strategies_per_player):
        equilibria = []

        # Iterăm prin TOATE profilurile posibile de strategii
        all_profiles = payoffs.keys()

        for profile in all_profiles:
            is_nash = True
            current_payoffs = payoffs[profile]  # Ex: (3, 5, 1) pentru profilul (0, 1, 0)

            # Verificăm pentru FIECARE jucător 'i' dacă poate devia unilateral
            for player_idx in range(num_players):
                player_current_strategy = profile[player_idx]
                player_current_payoff = current_payoffs[player_idx]

                # Căutăm o strategie alternativă pentru acest jucător
                can_improve = False
                for alt_strat in range(strategies_per_player):
                    if alt_strat == player_current_strategy:
                        continue

                    # Construim profilul ipotetic unde doar jucătorul 'i' schimbă
                    alt_profile_list = list(profile)
                    alt_profile_list[player_idx] = alt_strat
                    alt_profile = tuple(alt_profile_list)

                    # Vedem cât ar câștiga jucătorul 'i' în noul scenariu
                    alt_payoff = payoffs[alt_profile][player_idx]

                    if alt_payoff > player_current_payoff:
                        can_improve = True
                        break  # Am găsit o mișcare mai bună, deci nu e Nash

                if can_improve:
                    is_nash = False
                    break  # Dacă un singur jucător pleacă, profilul nu e Nash

            if is_nash:
                equilibria.append(f"Profil {profile} -> Payoffs {current_payoffs}")

        return equilibria if equilibria else ["Niciun echilibru Nash pur"]


# ==========================================
# 3. QUESTION GENERATOR ENGINE
# ==========================================

class QuestionBundle:
    """Holds everything needed: The question text and the computed answer."""

    def __init__(self, question_text, correct_answer_text, topic_info):
        self.question_text = question_text
        self.correct_answer_text = correct_answer_text
        self.topic_info = topic_info


class ContentGenerator:
    def __init__(self):
        self.engine = GameEngine()

    def create_question(self, topic_key, topic_data):
        """Factory method to dispatch based on topic type."""

        # 1. Handle Tree Games (Minimax)
        if topic_data.get("type") == "tree_game":
            return self._create_minimax_bundle(topic_data)

        # 2. Handle Matrix Games (Nash)
        elif topic_data.get("type") == "matrix_game":
            return self._create_nash_bundle(topic_data)

        # 3. Handle CSP/Search Strategy with real instances
        elif topic_data.get("type") in ["csp", "search_strategy"]:
            return self._create_strategy_bundle(topic_key, topic_data)

        # 4. Handle Theory Questions (Default)
        else:
            return self._create_theory_bundle(topic_key, topic_data)

    def _create_minimax_bundle(self, info):
        # Generate Data First
        depth = random.randint(2, 3)
        branching = 2
        tree = self.engine.generate_random_tree(depth, branching)

        # Solve Data
        root_val, visited = self.engine.solve_alpha_beta(tree)

        # Format Text
        tree_str = self.engine.tree_to_ascii(tree)
        question = (
            f"Se dă următorul arbore de joc (Rădăcina este MAX):\n\n{tree_str}\n\n"
            f"1. Care este valoarea în rădăcină folosind MinMax?\n"
            f"2. Câte noduri FRUNZĂ sunt vizitate dacă aplicăm Alpha-Beta Pruning (stânga-dreapta)?"
        )

        answer = (
            f"Valoarea în rădăcină este {root_val}. "
            f"Numărul de frunze vizitate cu Alpha-Beta este {visited}."
        )

        return QuestionBundle(question, answer, info)

    # def _create_nash_bundle(self, info):
    #     # Generate Data
    #     matrix = self.engine.generate_nash_matrix()
    #
    #     # Solve Data
    #     solutions = self.engine.solve_nash(matrix)
    #     solutions_str = "; ".join(solutions)
    #
    #     # Format Text
    #     mat_str = self.engine.format_matrix(matrix)
    #     question = (
    #         f"Pentru jocul în formă normală de mai jos (tuplele sunt (J1, J2)):\n{mat_str}\n"
    #         f"Identifică toate echilibrele Nash pure."
    #     )
    #
    #     answer = f"Echilibrele Nash sunt: {solutions_str}."
    #
    #     return QuestionBundle(question, answer, info)

    def _create_nash_bundle(self, info):
        # 1. Configurare
        num_players = random.randint(2, 3)  # Acum suportă 2 sau 3 jucători random
        strategies = 2

        # 2. Generare Date (folosind noua logică)
        # Nota: Va trebui sa instanțiezi clasa nouă sau să muți metodele în GameEngine
        game_data, strat_count = GameEngine.generate_n_player_game(num_players, strategies)

        # 3. Rezolvare
        solutions = GameEngine.solve_n_player_nash(game_data, num_players, strat_count)
        solutions_str = "; ".join(solutions)

        # 4. Formatare Text
        # Pentru 3 jucători, nu mai afișăm matricea, ci lista de profile, altfel e ilizibil
        if num_players == 2:
            # Putem converti înapoi la matrice pentru afișare frumoasă dacă vrei,
            # sau folosim formatarea simplă listată
            viz_str = GameEngine.format_n_player_game(game_data, num_players)
        else:
            viz_str = GameEngine.format_n_player_game(game_data, num_players)

        question = (
            f"Se dă un joc cu {num_players} jucători, fiecare având {strategies} strategii (0 sau 1).\n"
            f"Lista completă a câștigurilor (Payoffs) este:\n\n{viz_str}\n\n"
            f"Identifică toate echilibrele Nash pure."
        )

        answer = f"Echilibrele Nash sunt: {solutions_str}."

        return QuestionBundle(question, answer, info)

    def _create_theory_bundle(self, key, info):
        templates = [
            ("De ce este {strat} o strategie bună pentru {prob}?",
             "{strat} este utilă pentru {prob} deoarece {desc}."),

            ("Ce optimizări se pot aplica la {prob}?",
             "Pentru {prob} se pot folosi: {opts}."),
        ]

        q_temp, a_temp = random.choice(templates)
        strat = random.choice(info["strategies"]) if info["strategies"] else "aceasta strategie"

        q_text = q_temp.format(strat=strat, prob=key.replace("_", " "))
        a_text = a_temp.format(strat=strat, prob=key.replace("_", " "),
                               desc=info["description"],
                               opts=", ".join(info["optimizations"]))

        return QuestionBundle(q_text, a_text, info)

    def _create_strategy_bundle(self, key, info):
        """Generate strategy selection questions with real problem instances."""
        
        if "n-queens" in key:
            return self._create_nqueens_strategy(key, info)
        elif "knight" in key:
            return self._create_knight_tour_strategy(key, info)
        elif "graph_coloring" in key:
            return self._create_graph_coloring_strategy(key, info)
        elif "hanoi" in key:
            return self._create_hanoi_strategy(key, info)
        else:
            # Fallback to theory bundle
            return self._create_theory_bundle(key, info)

    def _create_nqueens_strategy(self, key, info):
        """Generate N-Queens strategy question with a specific board state."""
        n = random.randint(4, 6)
        
        # Example: board state shown as positions of conflicting queens
        question = (
            f"Pentru problema N-Queens cu N={n}:\n"
            f"Trei regine sunt deja plasate și crează conflicte. Cum rezolvi mai eficient?\n"
            f"A) Backtracking cu Forward Checking\n"
            f"B) Local Search (min-conflicts)\n"
            f"C) Genetic Algorithms\n"
            f"Justifică alegerea."
        )
        
        answer = (
            f"Răspuns: A) Backtracking cu Forward Checking. Motivare: "
            f"Pentru N={n} cu conflicte initiale, Forward Checking elimina rapid valori imposibile "
            f"(MRV heuristic) și reduce spațiul de căutare exponențial. "
            f"Local Search ar putea rămâne într-un optim local, iar GA-urile sunt excesive pentru probleme mici. "
            f"Backtracking garantează soluție."
        )
        
        return QuestionBundle(question, answer, info)

    def _create_knight_tour_strategy(self, key, info):
        """Generate Knight's Tour strategy question with a specific board size."""
        board_size = random.randint(6, 8)
        
        question = (
            f"Pentru problema Knight's Tour pe o tablă de {board_size}x{board_size}:\n"
            f"Calaretul pornind din colțul stânga-sus trebuie să viziteze fiecare pătrat exact o dată. "
            f"Care este cea mai bună abordare?\n"
            f"A) Backtracking pur (DFS)\n"
            f"B) Backtracking cu heuristica Warnsdorff (MRV)\n"
            f"C) Backtracking cu Forward Checking\n"
            f"Justifică alegerea."
        )
        
        answer = (
            f"Răspuns: B) Backtracking cu heuristica Warnsdorff. Motivare: "
            f"Pentru o tablă de {board_size}x{board_size}, backtracking pur explorează exponențial multe ramuri. "
            f"Warnsdorff prioritizează mutări către pătrate cu mai puține opțiuni viitoare (MRV heuristic), "
            f"reducând drastic backtracking. Această strategie găsește soluția în timp liniar pentru tablele obișnuite. "
            f"Forward Checking ajută mai puțin aici decât Warnsdorff pentru această problemă specifică."
        )
        
        return QuestionBundle(question, answer, info)

    def _create_graph_coloring_strategy(self, key, info):
        """Generate graph coloring strategy question with a specific graph."""
        num_nodes = random.randint(5, 8)
        density = random.choice(["rară", "medie", "densă"])
        
        question = (
            f"Un graf cu {num_nodes} noduri și conexiuni {density} trebuie colorat cu numarul minim de culori. "
            f"Alege strategia optimă:\n"
            f"A) CSP cu AC-3 (Arc Consistency)\n"
            f"B) Greedy coloring (First-Fit)\n"
            f"C) Backtracking fără propagare\n"
            f"Justifică alegerea considerând complexitatea și garantiile de optimalitate."
        )
        
        answer = (
            f"Răspuns: A) CSP cu AC-3. Motivare: "
            f"AC-3 propagă constrângeri înainte de backtracking, eliminând combinații imposibile. "
            f"Pentru grafuri cu {num_nodes} noduri și densitate {density}, "
            f"reduce spaţiul de căutare semnificativ. Greedy poate da soluții suboptimale (nu garantează min). "
            f"Backtracking pur fără AC-3 explorează mai multe noduri. "
            f"AC-3 este standard pentru CSP și optimizează atât viteza cât și calitatea soluției."
        )
        
        return QuestionBundle(question, answer, info)

    def _create_hanoi_strategy(self, key, info):
        """Generate Hanoi strategy question with a specific number of discs."""
        num_discs = random.randint(4, 6)
        
        question = (
            f"Pentru Problema Turnurilor din Hanoi cu {num_discs} discuri "
            f"și limitarea că fiecare mișcare trebuie executată în <1 ms:\n"
            f"A) Recursion pură (slow)\n"
            f"B) Recursion cu memoization (DP)\n"
            f"C) Iterativ cu stivă\n"
            f"Care abordare alegi și de ce?"
        )
        
        answer = (
            f"Răspuns: C) Iterativ cu stivă (sau B cu memoization ca alternativă). Motivare: "
            f"Pentru {num_discs} discuri, recursion pură necesită 2^{num_discs}-1 = {2**num_discs - 1} pași, "
            f"dar stack overflow se riscă cu recursie adâncă. "
            f"Memoization ajută dar nu elimina overhead recursiv. "
            f"Iterativ cu stivă este mai rapid (O(2^n) time dar fără overhead funcții) și garantează "
            f"<1 ms pe mașini moderne. Pentru {num_discs} discuri, iterativ execută instant."
        )
        
        return QuestionBundle(question, answer, info)

    def generate_problem_selection_question(self):
        """
        Generate a question where user identifies the problem type from a list of 4+
        and receives one or multiple instances, then must choose optimal strategy.
        Only generates the question (instance), NO pre-computed answer.
        """
        # Define the 4+ problems with their instances
        problems = {
            "n-queens": {
                "name": "N-Queens",
                "description": "Problema de a plasa N regine pe o tablă de șah",
                "instance_generator": lambda: {
                    "n": random.randint(4, 6),
                    "conflicts": random.randint(1, 3)
                },
                "strategies": [
                    "Backtracking cu Forward Checking",
                    "Local Search (Min-Conflicts)",
                    "Genetic Algorithms"
                ]
            },
            "knight_tour": {
                "name": "Knight's Tour",
                "description": "Parcurgerea unei table de șah cu calul",
                "instance_generator": lambda: {
                    "board_size": random.randint(6, 8),
                    "start_position": (0, 0)
                },
                "strategies": [
                    "Backtracking pur (DFS)",
                    "Backtracking cu heuristica Warnsdorff",
                    "Backtracking cu Forward Checking"
                ]
            },
            "graph_coloring": {
                "name": "Graph Coloring",
                "description": "Colorarea unui graf cu numărul minim de culori",
                "instance_generator": lambda: {
                    "num_nodes": random.randint(5, 8),
                    "density": random.choice(["rară", "medie", "densă"])
                },
                "strategies": [
                    "CSP cu AC-3 (Arc Consistency)",
                    "Greedy Coloring (First-Fit)",
                    "Backtracking fără propagare"
                ]
            },
            "hanoi": {
                "name": "Generalized Hanoi",
                "description": "Mutarea unui stack de discuri între tije cu constrângeri",
                "instance_generator": lambda: {
                    "num_discs": random.randint(4, 6),
                    "num_pegs": random.randint(3, 5)
                },
                "strategies": [
                    "Recursion pură",
                    "Recursion cu memoization (DP)",
                    "Iterativ cu stivă"
                ]
            }
        }

        # Select a random problem
        problem_key = random.choice(list(problems.keys()))
        problem = problems[problem_key]

        # Generate instance(s)
        instance = problem["instance_generator"]()

        # Format the question
        question_text = self._format_problem_selection_question(problem_key, problem, instance)

        # Return a bundle with question only (answer is None for user evaluation)
        # We'll use None as correct_answer_text to signal this is open-ended
        return QuestionBundle(
            question_text=question_text,
            correct_answer_text=None,  # No pre-computed answer
            topic_info={
                "type": "problem_selection",
                "problem": problem_key,
                "instance": instance,
                "strategies": problem["strategies"]
            }
        )

    def _format_problem_selection_question(self, problem_key, problem, instance):
        """Format the question text based on problem type and instance."""
        
        if problem_key == "n-queens":
            return (
                f"PROBLEMA: {problem['name']}\n"
                f"Descriere: {problem['description']}\n\n"
                f"INSTANȚĂ: N = {instance['n']}, cu {instance['conflicts']} regine deja plasate care creează conflicte.\n\n"
                f"ÎNTREBARE: Care este cea mai potrivită strategie de rezolvare?\n"
                f"Opțiuni:\n"
                f"A) {problem['strategies'][0]}\n"
                f"B) {problem['strategies'][1]}\n"
                f"C) {problem['strategies'][2]}\n\n"
                f"Justifică alegerea considerând complexitatea și eficiență."
            )

        elif problem_key == "knight_tour":
            return (
                f"PROBLEMA: {problem['name']}\n"
                f"Descriere: {problem['description']}\n\n"
                f"INSTANȚĂ: Tablă de {instance['board_size']}x{instance['board_size']}, "
                f"pornind din colțul stânga-sus {instance['start_position']}.\n\n"
                f"ÎNTREBARE: Care este cea mai potrivită strategie de rezolvare?\n"
                f"Opțiuni:\n"
                f"A) {problem['strategies'][0]}\n"
                f"B) {problem['strategies'][1]}\n"
                f"C) {problem['strategies'][2]}\n\n"
                f"Justifică alegerea considerând performanța și rata de succes."
            )

        elif problem_key == "graph_coloring":
            return (
                f"PROBLEMA: {problem['name']}\n"
                f"Descriere: {problem['description']}\n\n"
                f"INSTANȚĂ: Graf cu {instance['num_nodes']} noduri și conexiuni {instance['density']}.\n\n"
                f"ÎNTREBARE: Care este cea mai potrivită strategie de rezolvare?\n"
                f"Opțiuni:\n"
                f"A) {problem['strategies'][0]}\n"
                f"B) {problem['strategies'][1]}\n"
                f"C) {problem['strategies'][2]}\n\n"
                f"Justifică alegerea considerând optimalitate și complexitate."
            )

        elif problem_key == "hanoi":
            return (
                f"PROBLEMA: {problem['name']}\n"
                f"Descriere: {problem['description']}\n\n"
                f"INSTANȚĂ: {instance['num_discs']} discuri de diferite dimensiuni, "
                f"{instance['num_pegs']} tije disponibile.\n\n"
                f"ÎNTREBARE: Care este cea mai potrivită strategie de rezolvare?\n"
                f"Opțiuni:\n"
                f"A) {problem['strategies'][0]}\n"
                f"B) {problem['strategies'][1]}\n"
                f"C) {problem['strategies'][2]}\n\n"
                f"Justifică alegerea considerând eficiență și garantii de corectitudine."
            )

        # Default fallback
        return (
            f"PROBLEMA: {problem['name']}\n"
            f"Descriere: {problem['description']}\n\n"
            f"INSTANȚĂ: {instance}\n\n"
            f"ÎNTREBARE: Care este cea mai potrivită strategie din list?\n"
            f"Opțiuni:\n"
            f"A) {problem['strategies'][0]}\n"
            f"B) {problem['strategies'][1]}\n"
            f"C) {problem['strategies'][2]}\n\n"
            f"Justifică alegerea."
        )


# ==========================================
# 4. EVALUATOR
# ==========================================

class Evaluator:
    @staticmethod
    def normalize(text):
        return text.lower().replace("ă", "a").replace("î", "i").replace("ș", "s").replace("ț", "t")

    @staticmethod
    def cosine_similarity(s1, s2):
        # Simple implementation for dependency-free run
        def get_vec(text):
            words = re.findall(r'\w+', Evaluator.normalize(text))
            vec = {}
            for w in words: vec[w] = vec.get(w, 0) + 1
            return vec

        v1, v2 = get_vec(s1), get_vec(s2)
        intersection = set(v1.keys()) & set(v2.keys())
        numerator = sum([v1[x] * v2[x] for x in intersection])

        sum1 = sum([v1[x] ** 2 for x in v1.keys()])
        sum2 = sum([v2[x] ** 2 for x in v2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator: return 0.0
        return numerator / denominator

    def evaluate(self, user_answer: str, system_bundle: dict) -> dict:
        # Sigur că avem dict, nu obiect
        correct_answer_text = system_bundle.get("correct_answer_text", "")

        # 1. Similarity Check
        sim_score = self.cosine_similarity(user_answer, correct_answer_text)

        # 2. Keyword/Number Extraction Check (Hard check for Math problems)
        score = int(sim_score * 100)
        feedback = f"Similaritate semantică: {score}/100."

        user_norm = Evaluator.normalize(user_answer)
        sys_norm = Evaluator.normalize(system_bundle.correct_answer_text)

        # Extra logic for numeric answers (MinMax) -- FOR MINIMAX
        if "vizitate" in system_bundle.correct_answer_text:
            nums_sys = re.findall(r'\d+', system_bundle.correct_answer_text)
            nums_user = re.findall(r'\d+', user_answer)
            # Check if the numbers in correct answer appear in user answer
            if set(nums_sys).issubset(set(nums_user)):
                score = 100
                feedback = "Corect! Ai identificat valorile numerice corecte."
            elif not nums_user:
                score = 0
                feedback = "Nu ai introdus nicio valoare numerică."

        def parse_tuple(text_chunk):
            # Caută toate secvențele de cifre, ignorând paranteze, litere sau virgule
            nums = [int(n) for n in re.findall(r'\d+', text_chunk)]
            return tuple(nums) if nums else None

        if "echilibr" in sys_norm or "strategii" in sys_norm:

            sys_pattern = r'(?:Profil|Strategii|Row|Col)\s*[:]?\s*([\[\(].*?[\]\)])'
            raw_sys_matches = re.findall(sys_pattern, system_bundle.correct_answer_text)

            if not raw_sys_matches:
                clean_text = re.sub(r'Payoffs\s*[\[\(].*?[\]\)]', '', system_bundle.correct_answer_text,
                                    flags=re.IGNORECASE)
                raw_sys_matches = re.findall(r'[\[\(].*?[\]\)]', clean_text)

            correct_coords = set()
            for m in raw_sys_matches:
                t = parse_tuple(m)
                if t: correct_coords.add(t)

            raw_user_matches = re.findall(r'[\[\(].*?[\]\)]', user_answer)
            user_coords = set()

            if not raw_user_matches and re.search(r'\d', user_answer):
                t = parse_tuple(user_answer)
                if t: user_coords.add(t)
            else:
                for m in raw_user_matches:
                    t = parse_tuple(m)
                    if t: user_coords.add(t)

            if not correct_coords:
                negations = ["nu", "niciun", "none", "nimic", "zero", "inexistent"]
                has_negation = any(neg in user_norm for neg in negations)

                if has_negation:
                    score = 100
                    feedback = "Corect! Ai identificat că nu există niciun echilibru Nash pur."
                elif user_coords:
                    score = 0
                    feedback = "Greșit. Ai găsit echilibre, dar corect este că nu există."
                else:
                    feedback = f"Nu există echilibre. Similaritate răspuns: {score}%."

            else:
                if user_coords:
                    matched = user_coords & correct_coords

                    if len(matched) == len(correct_coords) and len(user_coords) == len(correct_coords):
                        score = 100
                        feedback = "Excelent! Ai identificat toate echilibrele corect."
                    elif matched:
                        ratio = len(matched) / len(correct_coords)
                        score = int(30 + (ratio * 70))
                        feedback = f"Parțial corect. Ai găsit {len(matched)} din {len(correct_coords)} echilibre."
                    else:
                        score = int(sim_score * 50)
                        feedback = f"Coordonatele propuse {list(user_coords)} nu sunt corecte. Corect era: {list(correct_coords)}."
                else:
                    feedback = f"Nu ai oferit coordonatele specifice (ex: (1, 1)). Similaritate text: {score}%."

        return {
            "score": score,
            "feedback": feedback,
            "correct_answer": correct_answer_text
        }


# ==========================================
# 5. MAIN PIPELINE
# ==========================================

def get_topic_from_prompt(prompt):
    p_norm = prompt.lower()
    
    # Check for course requests (c1, c2, c3)
    if "c1" in p_norm or "curs 1" in p_norm or "search" in p_norm:
        course = KNOWLEDGE_BASE["C1: Search Problems"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]
    elif "c2" in p_norm or "curs 2" in p_norm or "csp" in p_norm or "constraint" in p_norm:
        course = KNOWLEDGE_BASE["C2: Constraint Satisfaction"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]
    elif "c3" in p_norm or "curs 3" in p_norm or "game" in p_norm or "teorie" in p_norm:
        course = KNOWLEDGE_BASE["C3: Game Theory"]
        topic_key = random.choice(list(course.keys()))
        return topic_key, course[topic_key]
    
    # Check for specific topic synonyms
    for topic_key, synonyms in SYNONYMS.items():
        if any(s in p_norm for s in synonyms):
            # Search in KB
            for course in KNOWLEDGE_BASE.values():
                if topic_key in course:
                    return topic_key, course[topic_key]
    
    # Fallback default
    return "minmax_alphabeta", KNOWLEDGE_BASE["C3: Game Theory"]["minmax_alphabeta"]



from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

generator = ContentGenerator()
evaluator = Evaluator()

@app.route("/api/message",methods=["POST"])
def question():

    prompt = request.get_json().get("message","")

    # if not prompt or "owner" not in prompt or "value" not in prompt:
    #     return jsonify({"error": "Invalid payload"}), 400

    # adaugă id simplu (poți folosi uuid)
    # import uuid
    # new_message = {
    #     "id": str(uuid.uuid4()),
    #     "owner": prompt["owner"],
    #     "value": prompt["value"]
    # }
    # messages.append(new_message)

    import re

    # caută 'nr de intrebari' urmat de spațiu și un număr
    match = re.search(r"(\d+)\s+intrebari", prompt, re.IGNORECASE)

    nr_intrebari = 1
    if match:
        nr_intrebari = int(match.group(1))

    else:
        nr_intrebari = 1

    questions = []

    for i in range(nr_intrebari):

        if any(keyword in prompt.lower() for keyword in ["selectie problema", "alegere", "problem selection"]):
            print("--- Tip: Alegere dintre 4+ probleme cu instanță ---")
            bundle = generator.generate_problem_selection_question()
            
            # Display Question
            print(f"\n[AI Question]:\n{bundle.question_text}")

            questions.append({
            "question": bundle.question_text,
            "answer": bundle.correct_answer_text,
            "topic": bundle.topic_info,
        })
        else:
            # 1. Identify Topic
            topic_key, topic_data = get_topic_from_prompt(prompt)
            print(f"--- Subiect identificat: {topic_key} ---")

            # 2. Generate Bundle (Question + Pre-computed Answer)
            bundle = generator.create_question(topic_key, topic_data)

            questions.append({
            "question": bundle.question_text,
            "answer": bundle.correct_answer_text,
            "topic": bundle.topic_info,
        })

    return jsonify({"questions": questions}), 200


@app.route("/api/evaluate",methods=["POST"])
def score():

    data = request.get_json()

    print(data.get("bundle",""))

    resultat = evaluator.evaluate(data.get("response",""),data.get("bundle",""))
    return jsonify(resultat)

if __name__ == "__main__":
    app.run(port=3000, debug=True)