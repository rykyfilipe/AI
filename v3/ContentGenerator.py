import random
from v3.GameEngine import GameEngine
from v3.QuestionBundle import QuestionBundle

from v3.CSP import solve_from_partial_assignment

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

        # 4. Handle CSP Continuation Questions
        elif topic_data.get("type") == "csp_continuation":
            return self._create_csp_continuation_bundle(topic_key, topic_data)

        # 5. Handle Theory Questions (Default)
        else:
            return self._create_theory_bundle(topic_key, topic_data)

    def _create_csp_continuation_bundle(self, key, info):
        """
        Generează:
        - variabile
        - domenii
        - constrângeri
        - asignare parțială
        - metodă: FC / MRV / AC-3
        """

        # -------------------------
        # 1. INSTANȚĂ CSP
        # -------------------------
        variables = ["A", "B", "C", "D"]

        domains = {
            "A": [1, 2, 3],
            "B": [1, 2, 3],
            "C": [1, 2, 3],
            "D": [1, 2, 3]
        }

        # Constrângeri: diferite
        constraints = {
            ("A", "B"): lambda a, b: a != b,
            ("B", "C"): lambda b, c: b != c,
            ("C", "D"): lambda c, d: c != d,
            ("A", "D"): lambda a, d: a != d,
        }

        # Asignare parțială
        partial_assignment = {
            "A": random.choice([1, 2, 3])
        }

        # Metodă aleasă
        method = random.choice(["FC", "MRV", "AC3"])

        # -------------------------
        # 2. REZOLVARE
        # -------------------------
        try:
            from CSP import solve_from_partial_assignment
            solution = solve_from_partial_assignment(
                variables,
                domains,
                constraints,
                partial_assignment,
                method=method
            )
        except Exception as e:
            solution = None

        # -------------------------
        # 3. FORMATARE ÎNTREBARE
        # -------------------------
        question = (
            "Se dau următoarele elemente ale unui CSP:\n\n"
            f"Variabile: {variables}\n"
            f"Domenii: {domains}\n"
            f"Constrângeri: A≠B, B≠C, C≠D, A≠D\n"
            f"Asignantă parțială: {partial_assignment}\n\n"
            f"Cerință:\n"
            f"Care va fi asignarea variabilelor rămase folosind "
            f"Backtracking cu optimizarea {method}?"
        )

        # -------------------------
        # 4. FORMATARE RĂSPUNS
        # -------------------------
        if solution:
            answer = (
                f"Folosind Backtracking cu {method}, "
                f"se obține asignarea completă:\n{solution}"
            )
        else:
            answer = (
                f"Folosind Backtracking cu {method}, "
                f"instanța nu admite soluție."
            )

        return QuestionBundle(
            question_text=question,
            correct_answer_text=answer,
            topic_info={
                "type": "csp_continuation",
                "variables": variables,
                "domains": domains,
                "constraints": "A≠B, B≠C, C≠D, A≠D",
                "partial_assignment": partial_assignment,
                "method": method
            }
        )

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
        """Generate N-Queens strategy question and solve it using CSP logic."""
        n = random.randint(4, 6)
        
        # 1. Pregătire date pentru CSP (Variabile pe rânduri)
        variables = [f"R{i}" for i in range(n)]
        domains = {v: list(range(n)) for v in variables}
        
        constraints = {}
        for i in range(n):
            for j in range(i + 1, n):
                # r1, r2 sunt indecșii rândurilor, c1, c2 sunt coloanele (valorile)
                def make_check(r1, r2):
                    return lambda c1, c2: c1 != c2 and abs(c1 - c2) != abs(r1 - r2)
                constraints[(f"R{i}", f"R{j}")] = make_check(i, j)

        # 2. Rezolvare folosind motorul CSP (metoda FC - Forward Checking)
        solution = solve_from_partial_assignment(variables, domains, constraints, {}, method="FC")

        question = (
            f"PROBLEMA: N-Queens cu N={n}\n"
            f"Descriere: Plasarea a {n} regine pe tablă fără a se ataca.\n\n"
            f"ÎNTREBARE: Care este cea mai potrivită strategie de rezolvare?\n"
            f"A) Backtracking cu Forward Checking\n"
            f"B) Local Search (min-conflicts)\n"
            f"C) Genetic Algorithms\n\n"
            f"Justifică alegerea și oferă o soluție validă sub formă de coloane."
        )

        answer = (
            f"Răspuns: A) Backtracking cu Forward Checking. Motivare: "
            f"Pentru N={n}, FC elimină rapid ramurile imposibile (MRV heuristic) și reduce spațiul de căutare. "
            f"Soluție validă: {solution}."
        )

        return QuestionBundle(question, answer, info)

    def _create_graph_coloring_strategy(self, key, info):
        """Generate graph coloring strategy question and solve it using CSP logic."""
        num_nodes = random.randint(4, 5)
        nodes = [f"N{i}" for i in range(num_nodes)]
        colors = ["Rosu", "Verde", "Albastru"]
        
        # Generăm muchii aleatorii pentru instanță
        edges = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if random.random() > 0.4:
                    edges.append((nodes[i], nodes[j]))

        # 1. Pregătire date pentru CSP
        variables = nodes
        domains = {node: list(colors) for node in nodes}
        constraints = {}
        for edge in edges:
            constraints[edge] = lambda c1, c2: c1 != c2

        # 2. Rezolvare folosind motorul CSP (metoda AC3)
        solution = solve_from_partial_assignment(variables, domains, constraints, {}, method="AC3")

        question = (
            f"PROBLEMA: Graph Coloring\n"
            f"Noduri: {nodes}\n"
            f"Muchii: {edges}\n"
            f"Culori: {colors}\n\n"
            f"ÎNTREBARE: Ce strategie alegi pentru a garanta consistența înainte de căutare?\n"
            f"A) CSP cu AC-3 (Arc Consistency)\n"
            f"B) Greedy Coloring\n"
            f"C) Backtracking simplu\n\n"
            f"Justifică alegerea."
        )

        answer = (
            f"Răspuns: A) CSP cu AC-3. Motivare: AC-3 propagă constrângerile prin toate arcele grafului, "
            f"eliminând culorile care nu pot face parte dintr-o soluție validă. "
            f"Soluție detectată: {solution if solution else 'Nicio solutie cu 3 culori'}"
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
            f"Pentru {num_discs} discuri, recursion pură necesită 2^{num_discs}-1 = {2 ** num_discs - 1} pași, "
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